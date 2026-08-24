import { api } from "@/lib/axios";
import type { FetchEventsParams, Event } from "../types";
import { ROUTES } from "@/constants/routes";

export async function fetchEvents(params?: FetchEventsParams): Promise<Event[]> {
  const response = await api.get<Event[]>(ROUTES.EVENTS.GET_ALL, { params });
  return response.data;
}

export async function fetchEventById(id: string): Promise<Event> {
  const response = await api.get<Event>(ROUTES.EVENTS.GET_BY_ID(id));
  return response.data;
}
