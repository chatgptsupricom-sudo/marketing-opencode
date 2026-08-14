import axios from 'axios';

const RAW_URL = process.env.ODOO_URL || process.env.NEXT_PUBLIC_ODOO_URL || 'https://supricom2.odoo.com';
const ODOO_URL = RAW_URL.replace(/\/$/, '');
const ODOO_DB = process.env.ODOO_DB || 'supricom-prod1-25424683';
const ODOO_UID = parseInt(process.env.ODOO_UID || '388', 10);
const ODOO_API_KEY = process.env.ODOO_API_KEY || process.env.ODOO_PASSWORD || '';

// Sede → company_id en Odoo (del dashboard funcional)
const COMPANY_VALENCIA = parseInt(process.env.ODOO_COMPANY_VALENCIA || '9', 10);
const COMPANY_CARACAS = parseInt(process.env.ODOO_COMPANY_CARACAS || '10', 10);
const WAREHOUSE_VALENCIA = parseInt(process.env.ODOO_WAREHOUSE_VALENCIA || '9', 10);
const WAREHOUSE_CARACAS = parseInt(process.env.ODOO_WAREHOUSE_CARACAS || '10', 10);

let requestId = 1;

export async function callOdooRPC<T>(
  model: string,
  method: string,
  args: any[] = [],
  kwargs: Record<string, any> = {},
): Promise<T | null> {
  try {
    const payload = {
      jsonrpc: '2.0',
      method: 'call',
      params: {
        service: 'object',
        method: 'execute_kw',
        args: [
          ODOO_DB,
          ODOO_UID,
          ODOO_API_KEY,
          model,
          method,
          args,
          kwargs,
        ],
      },
      id: requestId++,
    };

    const response = await axios.post<{ jsonrpc: string; id: number; result?: T; error?: any }>(
      `${ODOO_URL}/jsonrpc`,
      payload,
      { headers: { 'Content-Type': 'application/json' }, timeout: 60000 },
    );

    if (response.data.error) {
      console.error('❌ Odoo RPC error:', response.data.error);
      throw new Error(`Odoo RPC error: ${JSON.stringify(response.data.error)}`);
    }

    return response.data.result as T;
  } catch (error: any) {
    console.error('❌ Error RPC:', error.message);
    if (axios.isAxiosError(error) && error.response?.data) {
      console.error('Response:', JSON.stringify(error.response.data).substring(0, 500));
    }
    throw error;
  }
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

interface RawProduct {
  id: number;
  default_code?: string | boolean;
  display_name?: string;
  name?: string;
  categ_id?: [number, string] | string;
  x_studio_marca?: [number, string] | string;
  company_sale_price?: number | boolean;
  product_tmpl_id?: [number, string] | number;
}

function normalizeName(p: RawProduct): string {
  return p.display_name || p.name || '';
}

function normalizeCategory(p: RawProduct): string {
  let catName = '';
  if (Array.isArray(p.categ_id)) {
    catName = p.categ_id[1] || '';
  } else {
    catName = String(p.categ_id || '');
  }
  return catName.toUpperCase().trim() || 'SIN CATEGORIA';
}

function normalizeBrand(p: RawProduct): string {
  let marcaName = '';
  if (Array.isArray(p.x_studio_marca)) {
    marcaName = p.x_studio_marca[1] || '';
  } else {
    marcaName = String(p.x_studio_marca || '');
  }
  return marcaName.trim() || 'SIN MARCA';
}

function normalizeSku(p: RawProduct): string {
  const code = p.default_code;
  return typeof code === 'string' ? code : '';
}

function normalizePrice(p: RawProduct): number {
  const price = p.company_sale_price;
  return typeof price === 'number' ? price : 0;
}

const EXCLUDED_CATEGORIES = [
  'ALL',
  'SERVICIO',
  'JUGUETES',
  'BOOKING FEES',
  'POS',
  'DELIVERIES',
  'EXPENSES',
  'SALEABLE',
  'SOFTWARE',
];

async function fetchProducts(companyId: number): Promise<RawProduct[]> {
  const productos = await callOdooRPC<any[]>(
    'product.product',
    'search_read',
    [
      [
        ['sale_ok', '=', true],
        ['active', '=', true],
        ['type', '=', 'product'],
      ],
    ],
    {
      fields: [
        'id',
        'display_name',
        'name',
        'product_tmpl_id',
        'default_code',
        'company_sale_price',
        'categ_id',
        'barcode',
        'uom_id',
        'x_studio_marca',
      ],
      limit: 5000,
      order: 'name asc',
      context: { allowed_company_ids: [companyId], lang: 'es_VE' },
    },
  );

  return productos || [];
}

async function fetchLocationIds(companyId: number, warehouseId: number): Promise<number[]> {
  const warehouseData = await callOdooRPC<any[]>(
    'stock.warehouse',
    'search_read',
    [[['id', '=', warehouseId]]],
    { fields: ['id', 'lot_stock_id'], limit: 1 },
  );
  const locId = warehouseData?.[0]?.lot_stock_id?.[0];
  return locId ? [locId] : [];
}

async function fetchStockByLocation(productIds: number[], locationIds: number[], companyId: number): Promise<Map<number, number>> {
  const stockMap = new Map<number, number>();
  if (productIds.length === 0) return stockMap;

  const domain: any[] = [['product_id', 'in', productIds]];
  if (locationIds.length > 0) {
    domain.push(['location_id', 'child_of', locationIds]);
  } else {
    domain.push(['location_id.usage', '=', 'internal']);
    domain.push(['company_id', '=', companyId]);
  }

  const stockData = await callOdooRPC<any[]>(
    'stock.quant',
    'search_read',
    [domain],
    { fields: ['product_id', 'quantity', 'reserved_quantity'], limit: 0 },
  );

  if (!stockData) return stockMap;

  for (const s of stockData) {
    if (!s.product_id) continue;
    const id = Array.isArray(s.product_id) ? s.product_id[0] : s.product_id;
    const qty = Math.max(0, (s.quantity || 0) - (s.reserved_quantity || 0));
    stockMap.set(id, (stockMap.get(id) || 0) + qty);
  }

  return stockMap;
}

async function fetchCatalogForSede(companyId: number, warehouseId: number): Promise<{ products: RawProduct[]; stock: Map<number, number> }> {
  const [products, locationIds] = await Promise.all([
    fetchProducts(companyId),
    fetchLocationIds(companyId, warehouseId),
  ]);

  const productIds = products.map((p) => p.id);
  const stock = await fetchStockByLocation(productIds, locationIds, companyId);

  return { products, stock };
}

export async function fetchCatalogo(): Promise<CatalogoData> {
  if (!ODOO_API_KEY) {
    throw new Error('ODOO_API_KEY no está configurado');
  }

  const [valenciaData, caracasData] = await Promise.all([
    fetchCatalogForSede(COMPANY_VALENCIA, WAREHOUSE_VALENCIA),
    fetchCatalogForSede(COMPANY_CARACAS, WAREHOUSE_CARACAS),
  ]);

  // Index products by ID for GENERAL aggregation
  const allProducts = new Map<number, RawProduct>();
  const valenciaStock = new Map<number, number>();
  const caracasStock = new Map<number, number>();

  for (const p of valenciaData.products) {
    allProducts.set(p.id, p);
    valenciaStock.set(p.id, valenciaData.stock.get(p.id) || 0);
  }

  for (const p of caracasData.products) {
    if (!allProducts.has(p.id)) {
      allProducts.set(p.id, p);
    }
    caracasStock.set(p.id, caracasData.stock.get(p.id) || 0);
  }

  const result: CatalogoData = {
    GENERAL: {},
    CARACAS: {},
    VALENCIA: {},
  };

  // Helper to add product to a region bucket
  const addToBucket = (region: keyof CatalogoData, p: RawProduct, qty: number) => {
    const categoria = normalizeCategory(p);
    if (EXCLUDED_CATEGORIES.some((ex) => categoria.includes(ex))) return;

    const producto: Producto = {
      sku: normalizeSku(p),
      nombre: normalizeName(p),
      marca: normalizeBrand(p),
      categoria,
      cantidad: qty,
      precio: normalizePrice(p),
    };

    if (!result[region][categoria]) result[region][categoria] = [];
    result[region][categoria].push(producto);
  };

  for (const [id, p] of Array.from(allProducts.entries())) {
    const valQty = valenciaStock.get(id) || 0;
    const carQty = caracasStock.get(id) || 0;
    const totalQty = valQty + carQty;
    const price = normalizePrice(p);

    // GENERAL: any product with stock in any sede and price > 1
    if (totalQty > 0 && price > 1) {
      addToBucket('GENERAL', p, totalQty);
    }

    // Per-sede: product with stock in that sede and price > 1
    if (carQty > 0 && price > 1) {
      addToBucket('CARACAS', p, carQty);
    }

    if (valQty > 0 && price > 1) {
      addToBucket('VALENCIA', p, valQty);
    }
  }

  // Sort categories and products within each region
  for (const region of Object.keys(result) as (keyof CatalogoData)[]) {
    const sortedRegion: Record<string, Producto[]> = {};
    const categories = Object.keys(result[region]).sort();
    for (const cat of categories) {
      sortedRegion[cat] = result[region][cat].sort((a, b) =>
        a.nombre.localeCompare(b.nombre, 'es', { sensitivity: 'base' }),
      );
    }
    result[region] = sortedRegion;
  }

  return result;
}
