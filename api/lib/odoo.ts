import https from 'https';
import { URL } from 'url';

const ODOO_URL = process.env.ODOO_URL!;
const ODOO_DB = process.env.ODOO_DB!;
const ODOO_USER = process.env.ODOO_USER!;
const ODOO_PASSWORD = process.env.ODOO_PASSWORD!;

function escapeXml(str: string): string {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function serializeValue(val: any): string {
  if (val === null || val === undefined) return '<nil/>';
  if (typeof val === 'boolean') return `<boolean>${val ? 1 : 0}</boolean>`;
  if (typeof val === 'number') return Number.isInteger(val) ? `<int>${val}</int>` : `<double>${val}</double>`;
  if (typeof val === 'string') return `<string>${escapeXml(val)}</string>`;
  if (Array.isArray(val)) {
    const items = val.map(v => `<value>${serializeValue(v)}</value>`).join('');
    return `<array><data>${items}</data></array>`;
  }
  if (typeof val === 'object') {
    const members = Object.entries(val)
      .map(([k, v]) => `<member><name>${k}</name><value>${serializeValue(v)}</value></member>`)
      .join('');
    return `<struct>${members}</struct>`;
  }
  return `<string>${escapeXml(String(val))}</string>`;
}

function xmlRpcCall(path: string, methodName: string, params: any[]): Promise<string> {
  return new Promise((resolve, reject) => {
    const paramXml = params.map(p => `<param><value>${serializeValue(p)}</value></param>`).join('');
    const body = `<?xml version="1.0"?><methodCall><methodName>${methodName}</methodName><params>${paramXml}</params></methodCall>`;

    const parsedUrl = new URL(ODOO_URL + path);
    const options = {
      hostname: parsedUrl.hostname,
      port: 443,
      path: parsedUrl.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'text/xml',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── Robust XML parser for Odoo responses ──

interface XmlNode {
  tag: string;
  text: string;
  children: XmlNode[];
}

function parseXmlNode(xml: string, start: number): { node: XmlNode; end: number } {
  // Find opening tag
  const openMatch = xml.substring(start).match(/^<(\w+)>/);
  if (!openMatch) return { node: { tag: '', text: xml.substring(start), children: [] }, end: xml.length };

  const tag = openMatch[1];
  const tagEnd = start + openMatch[0].length;

  // Self-closing tag
  if (xml.substring(tagEnd).startsWith('/>')) {
    return { node: { tag, text: '', children: [] }, end: tagEnd + 2 };
  }

  // Find closing tag
  let depth = 1;
  let pos = tagEnd;
  const children: XmlNode[] = [];
  let textContent = '';

  while (pos < xml.length && depth > 0) {
    const nextOpen = xml.indexOf('<', pos);
    const nextClose = xml.indexOf('>', pos);

    if (nextClose === -1) break;

    if (nextOpen !== -1 && nextOpen < nextClose) {
      // Check if it's a closing tag
      if (xml[nextOpen + 1] === '/') {
        const closeEnd = xml.indexOf('>', nextOpen);
        if (xml.substring(nextOpen + 2, closeEnd).trim() === tag) {
          depth--;
          if (depth === 0) {
            // Capture any text before the closing tag
            textContent = xml.substring(tagEnd, nextOpen).trim();
            pos = closeEnd + 1;
            break;
          }
        }
        pos = closeEnd + 1;
      } else {
        // It's an opening tag of a child
        const child = parseXmlNode(xml, nextOpen);
        children.push(child.node);
        pos = child.end;
      }
    } else {
      // Only a closing tag
      if (xml[nextOpen + 1] === '/') {
        const closeEnd = xml.indexOf('>', nextOpen);
        depth--;
        if (depth === 0) {
          textContent = xml.substring(tagEnd, nextOpen).trim();
          pos = closeEnd + 1;
          break;
        }
        pos = closeEnd + 1;
      } else {
        pos = nextClose + 1;
      }
    }
  }

  return { node: { tag, text: textContent, children }, end: pos };
}

function getNodeText(node: XmlNode): string {
  if (node.children.length === 0) return node.text;
  // Get text of first child if it's a simple text node
  for (const child of node.children) {
    if (child.tag === 'string' || child.tag === 'int' || child.tag === 'double' || child.tag === 'boolean') {
      return child.text || getNodeText(child);
    }
  }
  return node.text;
}

function findChildren(node: XmlNode, tag: string): XmlNode[] {
  return node.children.filter(c => c.tag === tag);
}

function findChild(node: XmlNode, tag: string): XmlNode | undefined {
  return node.children.find(c => c.tag === tag);
}

function parseArrayValue(node: XmlNode): any[] {
  const dataNode = findChild(node, 'data');
  if (!dataNode) return [];
  const valueNodes = findChildren(dataNode, 'value');
  return valueNodes.map(v => parseValue(v));
}

function parseValue(node: XmlNode): any {
  if (node.children.length === 0) {
    return node.text;
  }

  const firstChild = node.children[0];
  switch (firstChild.tag) {
    case 'int':
    case 'i4':
      return parseInt(firstChild.text || '0');
    case 'double':
      return parseFloat(firstChild.text || '0');
    case 'boolean':
      return (firstChild.text || '0') === '1';
    case 'string':
      return firstChild.text || '';
    case 'array':
      return parseArrayValue(firstChild);
    case 'struct':
      return parseStruct(firstChild);
    case 'nil':
      return null;
    default:
      return firstChild.text || '';
  }
}

function parseStruct(node: XmlNode): Record<string, any> {
  const result: Record<string, any> = {};
  const memberNodes = findChildren(node, 'member');

  for (const member of memberNodes) {
    const nameNode = findChild(member, 'name');
    const valueNode = findChild(member, 'value');
    if (nameNode && valueNode) {
      const name = nameNode.text || getNodeText(nameNode);
      result[name] = parseValue(valueNode);
    }
  }

  return result;
}

function parseResponse(xml: string): any {
  // Find the <value> inside <params><param>
  const valueStart = xml.indexOf('<value>');
  if (valueStart === -1) throw new Error('No <value> found in response');

  const { node } = parseXmlNode(xml, valueStart);
  return parseValue(node);
}

async function authenticate(): Promise<number> {
  const resp = await xmlRpcCall('/xmlrpc/2/common', 'authenticate', [ODOO_DB, ODOO_USER, ODOO_PASSWORD, {}]);
  const uid = parseResponse(resp);
  if (typeof uid !== 'number' || uid === 0) {
    throw new Error(`Authentication failed. Response: ${resp.substring(0, 500)}`);
  }
  return uid;
}

export interface Producto {
  sku: string;
  nombre: string;
  marca: string;
  categoria: string;
  cantidad: number;
  precio: number;
}

export type CatalogoData = {
  GENERAL: Record<string, Producto[]>;
  CARACAS: Record<string, Producto[]>;
  VALENCIA: Record<string, Producto[]>;
};

export async function fetchCatalogo(): Promise<CatalogoData> {
  const uid = await authenticate();

  const fields = ['default_code', 'name', 'categ_id', 'x_studio_marca', 'qty_available', 'company_sale_price'];

  const resp = await xmlRpcCall('/xmlrpc/2/object', 'execute_kw', [
    ODOO_DB,
    uid,
    ODOO_PASSWORD,
    'product.product',
    'search_read',
    [[]],
    { fields, limit: 2000, order: 'name asc' },
  ]);

  const rawProducts = parseResponse(resp);
  const products = Array.isArray(rawProducts) ? rawProducts : [];

  const result: CatalogoData = {
    GENERAL: {},
    CARACAS: {},
    VALENCIA: {},
  };

  for (const p of products) {
    // categ_id: [id, name] or just name
    let catName = '';
    if (Array.isArray(p.categ_id)) {
      catName = p.categ_id[1] || '';
    } else {
      catName = String(p.categ_id || '');
    }
    const cat = catName.toUpperCase().trim() || 'SIN CATEGORIA';

    // Filter out internal Odoo categories
    const excluded = ['ALL', 'SERVICIO', 'JUGUETES', 'ALL / SALEABLE / BOOKING FEES', 'ALL / SALEABLE / POS'];
    if (excluded.includes(cat)) continue;

    // x_studio_marca: [id, name] or just name
    let marcaName = '';
    if (Array.isArray(p.x_studio_marca)) {
      marcaName = p.x_studio_marca[1] || '';
    } else {
      marcaName = String(p.x_studio_marca || '');
    }
    const marca = marcaName.trim() || 'SIN MARCA';

    const stock = typeof p.qty_available === 'number' ? p.qty_available : 0;
    const precio = typeof p.company_sale_price === 'number' ? p.company_sale_price : 0;

    const prod: Producto = {
      sku: p.default_code || '',
      nombre: p.name || '',
      marca,
      categoria: cat,
      cantidad: stock,
      precio,
    };

    if (!result.GENERAL[cat]) result.GENERAL[cat] = [];
    result.GENERAL[cat].push(prod);

    // Split stock 50/50 for CARACAS / VALENCIA (placeholder until warehouse-level stock)
    const halfStock = Math.round(stock / 2);

    if (!result.CARACAS[cat]) result.CARACAS[cat] = [];
    result.CARACAS[cat].push({ ...prod, cantidad: stock - halfStock });

    if (!result.VALENCIA[cat]) result.VALENCIA[cat] = [];
    result.VALENCIA[cat].push({ ...prod, cantidad: halfStock });
  }

  return result;
}
