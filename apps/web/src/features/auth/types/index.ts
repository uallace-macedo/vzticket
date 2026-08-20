import { z } from 'zod'

export const userRoleSchema = z.enum(['organizer', 'client', 'gatekeeper']);
export type UserRole = z.infer<typeof userRoleSchema>;

export const userCreateSchema = z.object({
  name: z.string().min(3, 'Informe seu nome.'),
  email: z.email('Informe um email válido.'),
  role: userRoleSchema,
  password: z.string().min(6, 'A senha deve conter no mínimo 6 caracteres.')
});
export type UserCreateProps = z.infer<typeof userCreateSchema>;

export const userLoginSchema = z.object({
  username: z.string().min(1, 'Por favor, informe seu email.'),
  password: z.string().min(1, 'Por favor, informe sua senha.'),

  grant_type: z.string(),
  scope: z.string(),
  client_id: z.string(),
  client_secret: z.string()
});
export type UserLoginProps = z.infer<typeof userLoginSchema>;

export type User = {
  name: string;
  email: string;
  role: UserRole;
  id: string;
}

export type LoginResponse = User;
