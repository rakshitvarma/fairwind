const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8080";

export type RouteResponse = {
  category: string;
  source: string;
  tokens: number;
  elapsed: number;
  answer: string;
};

export async function routeTask(prompt: string): Promise<RouteResponse> {
  const res = await fetch(`${API_BASE}/api/route`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export type ModelsResponse = {
  fireworks_models: string[];
  local_models: { name: string; categories: string[] }[];
  has_fireworks_creds: boolean;
};

export async function getModels(): Promise<ModelsResponse> {
  const res = await fetch(`${API_BASE}/api/models`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getHealth(): Promise<{ status: string; local_general_available: boolean; local_code_available: boolean }> {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
