import { NextRequest, NextResponse } from 'next/server';
import { fetchCatalogo } from '@/lib/odoo';
import { validateApiKey } from '@/lib/auth';

// SIN CACHE: siempre consulta Odoo fresco para datos en vivo
// (antes tenia TTL de 24h que causaba datos desactualizados)

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'X-API-Key, Content-Type',
  'Access-Control-Max-Age': '86400',
};

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: CORS_HEADERS });
}

export async function GET(request: NextRequest) {
  if (!validateApiKey(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: CORS_HEADERS });
  }

  try {
    // SIEMPRE fetch fresco desde Odoo - sin cache intermedio
    const productos = await fetchCatalogo();

    return NextResponse.json({
      productos,
      actualizado: new Date().toISOString(),
    }, {
      headers: {
        ...CORS_HEADERS,
        'Cache-Control': 'no-store, no-cache, must-revalidate',
        'Pragma': 'no-cache',
      },
    });
  } catch (error: any) {
    console.error('Error fetching catalog:', error);
    return NextResponse.json(
      {
        error: 'Internal server error',
        message: error?.message || 'Unknown error',
      },
      { status: 500, headers: CORS_HEADERS }
    );
  }
}
