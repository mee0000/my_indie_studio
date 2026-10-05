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

export async function fetchDemands(): Promise<DemandPost[]> {
  // Vite 프록시 또는 직접 호출
  const response = await fetch('/api/v1/demands');
  if (!response.ok) {
    throw new Error('Failed to fetch demand posts');
  }
  return response.json();
}