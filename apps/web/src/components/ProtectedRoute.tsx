import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/features/auth/store/use-auth-store';
import { PAGES } from '@/constants/pages';

interface ProtectedRouteProps {
  requiredRole?: string;
}

export function ProtectedRoute({ requiredRole }: ProtectedRouteProps) {
  const { user } = useAuthStore();

  if (!user) {
    return <Navigate to={PAGES.PUBLIC.HOME} replace />;
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to={PAGES.PUBLIC.HOME} replace />;
  }

  return <Outlet />;
}