import { toast } from "sonner";
import { useForm } from "react-hook-form";
import { useAuthStore } from "../store/use-auth-store";
import { userCreateSchema, userLoginSchema, type LoginResponse, type UserCreateProps, type UserLoginProps } from "../types";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";

import { create, login, logout } from "../services/auth-service";
import { useNavigate, type ErrorResponse } from "react-router-dom";
import type { ValidationErrorResponse } from "@/constants/types";
import { PAGES } from "@/constants/pages";

export function useAuth() {
  const navigate = useNavigate();
  const { setUser, closeAuthModal } = useAuthStore();

  function getErrorMessage(error: unknown): string {
    const err = error as { response?: { data?: ErrorResponse | ValidationErrorResponse } };
    const responseData = err.response?.data;

    if (responseData) {
      if ('errors' in responseData && Array.isArray(responseData.errors) && responseData.errors.length > 0) {
        return responseData.errors[0].message;
      }

      if('detail' in responseData && typeof responseData.detail === 'string') {
        return responseData.detail;
      }
    }

    return 'Ocorreu um erro. Tente novamente mais tarde.'
  }

  // Forms
  const createForm = useForm<UserCreateProps>({
    resolver: zodResolver(userCreateSchema)
  })

  const loginForm = useForm<UserLoginProps>({
    resolver: zodResolver(userLoginSchema),
    defaultValues: {
      grant_type: 'password',
      client_id: '',
      client_secret: '',
      scope: ''
    }
  })

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data: UserCreateProps) => create(data),
    onSuccess: () => {
      createForm.reset();
      closeAuthModal();
      
      toast.success('Conta criada com sucesso! Faça seu login para continuar.')
    },
    onError: (error: unknown) => {
      toast.error(getErrorMessage(error))
    }
  })

  const loginMutation = useMutation({
    mutationFn: (data: UserLoginProps) => login(data),
    onSuccess: (user: LoginResponse) => {
      setUser(user);
      closeAuthModal();
      loginForm.reset();
      
      toast.success(`Bem-vindo(a) de volta, ${user.name}!`)
      navigate(PAGES.PUBLIC.EVENTS);
    },
    onError: (error: unknown) => {
      toast.error(getErrorMessage(error))
    }
  })

  const logoutMutation = useMutation({
    mutationFn: () => logout(),
    onSuccess: () => {
      setUser(null);
      
      toast.info('Sessão encerrada com sucesso.');
      navigate(PAGES.PUBLIC.HOME);
    }
  })

  return {
    create: {
      register: createForm.register,
      handleSubmit: createForm.handleSubmit((data: UserCreateProps) => createMutation.mutate(data)),
      errors: createForm.formState.errors,
      isPending: createMutation.isPending,
      isSuccess: createMutation.isSuccess
    },

    login: {
      register: loginForm.register,
      handleSubmit: loginForm.handleSubmit((data: UserLoginProps) => loginMutation.mutate(data)),
      errors: loginForm.formState.errors,
      isPending: loginMutation.isPending
    },

    logout: () => logoutMutation.mutate()
  }
}