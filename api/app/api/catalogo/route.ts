import { NextRequest, NextResponse } from 'next/server';
import { fetchCatalogo } from '@/lib/odoo';
import { validateApiKey } from '@/lib/auth';

let cache: { data: any; ts: number } | null = null;
const TTL = 24 * 60 * 60 * 1000; // 24 horas

export async function GET(request: NextRequest) {
  if (!validateApiKey(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    // Cache hit
    if (cache && Date.now() - cache.ts < TTL) {
      return NextResponse.json({
        productos: cache.data,
        actualizado: new Date(cache.ts).toISOString(),
      });
    }

    // Fetch from Odoo
    const productos = await fetchCatalogo();
    cache = { data: productos, ts: Date.now() };

    return NextResponse.json({
      productos,
      actualizado: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error fetching catalog:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
