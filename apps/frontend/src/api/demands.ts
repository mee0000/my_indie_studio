export interface DemandPost {
  id: number;
  user_id: number;
  title: string;
  category: string;
  target_price_krw: number;
  status: string;
  description?: string;
  created_at: string;
}

export interface CreateDemandPayload {
  title: string;
  category: "fashion" | "beauty" | "popup";
  target_price_krw: number;
  description?: string;
}

export async function fetchDemands(): Promise<DemandPost[]> {
  // Vite 프록시 또는 직접 호출
  const response = await fetch("/api/v1/demands");
  if (!response.ok) {
    throw new Error("Failed to fetch demand posts");
  }
  return response.json();
}

export async function createDemand(payload: CreateDemandPayload): Promise<DemandPost> {
  const response = await fetch("/api/v1/demands", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }
  return response.json();
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();
    return formatApiError(body);
  } catch {
    return "Failed to create demand post";
  }
}

function formatApiError(body: unknown): string {
  if (!body || typeof body !== "object" || !("detail" in body)) {
    return "Failed to create demand post";
  }
  const detail = (body as { detail: unknown }).detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (!Array.isArray(detail)) {
    return "Failed to create demand post";
  }
  const messages = detail
    .map((item) => {
      if (!item || typeof item !== "object" || !("msg" in item)) {
        return "";
      }
      const msg = String(item.msg);
      if (!("loc" in item) || !Array.isArray(item.loc)) {
        return msg;
      }
      const loc = item.loc.filter((part) => part !== "body").join(".");
      return loc ? `${loc}: ${msg}` : msg;
    })
    .filter(Boolean);
  return messages.join("; ") || "Failed to create demand post";
}
