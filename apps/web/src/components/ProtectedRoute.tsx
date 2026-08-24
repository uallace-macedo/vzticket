import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { PAGES } from '@/constants/pages';

interface ProtectedRouteProps {
  allowedRoles?: string[];
}

export function ProtectedRoute({ allowedRoles }: ProtectedRouteProps) {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to={PAGES.PUBLIC.HOME} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={PAGES.PUBLIC.HOME} replace />;
  }

  return <Outlet />;
}