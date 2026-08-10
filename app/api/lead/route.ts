import { NextResponse } from "next/server";

/**
 * Placeholder lead endpoint. Wire this to a CRM, sheet, or mailbox before
 * launch; for a fully static export, point the form at an external endpoint
 * instead and drop this route.
 */
export async function POST(request: Request) {
  const lead = await request.json().catch(() => null);
  if (!lead || !lead.phone) {
    return NextResponse.json({ ok: false, error: "invalid lead" }, { status: 400 });
  }
  console.log("[lead]", lead);
  return NextResponse.json({ ok: true });
}
