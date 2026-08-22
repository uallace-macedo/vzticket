import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "../components/Layout";
import { HomePage } from "@/features/home/pages/HomePage";
import { PAGES } from "@/constants/pages";
import { EventsPage } from "@/features/event/pages/EventsPage";
import { EventDetailPage } from "@/features/event/pages/EventDetailPage";
import { WalletPage } from "@/features/wallet/pages/WalletPage";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { OrganizerEventsPage } from "@/features/organizer/pages/OrganizerEventsPage";
import { CheckoutPage } from "@/features/ticket/pages/CheckoutPage";


export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<Layout showSearchInHeader={true} />}>
          <Route path={PAGES.PUBLIC.HOME} element={<HomePage />} />
          <Route path={PAGES.PUBLIC.EVENTS} element={<EventsPage />} />
          <Route path={PAGES.PUBLIC.EVENT} element={<EventDetailPage />} />
        </Route>

        {/* Private Routes */}
        <Route element={<Layout showSearchInHeader={false} />}>
          <Route element={<ProtectedRoute />}>
            <Route path={PAGES.PRIVATE.PROFILE} element={<h1>Minha Conta</h1>} />
            <Route path={PAGES.PRIVATE.TICKETS} element={<h1>Meus Ingressos</h1>} />
            <Route path={PAGES.PRIVATE.WALLET} element={<WalletPage />} />
            <Route path={PAGES.PRIVATE.EVENTS.CHECKOUT_BASE} element={<CheckoutPage />} />
          </Route>

          <Route element={<ProtectedRoute requiredRole="organizer" />}>
            <Route path={PAGES.PRIVATE.ORGANIZER.EVENTS} element={<OrganizerEventsPage /> } />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}