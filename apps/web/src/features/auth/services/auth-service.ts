import { api } from "@/lib/axios";
import type { LoginResponse, UserCreateProps, UserLoginProps } from "../types";
import { ROUTES } from "@/constants/routes";

export async function create(data: UserCreateProps) {
  const response = await api.post(ROUTES.AUTH.REGISTER, data);
  return response.data;
}

export async function login(data: UserLoginProps): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>(
    ROUTES.AUTH.LOGIN,
    data,
    { headers: {'Content-Type': 'application/x-www-form-urlencoded'} }
  );

  return response.data;
}

export async function logout() {
  const response = await api.post(ROUTES.AUTH.LOGOUT);
  return response;
}