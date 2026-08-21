import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "../components/Layout";
import { HomePage } from "@/features/home/pages/HomePage";
import { PAGES } from "@/constants/pages";
import { EventsPage } from "@/features/event/pages/EventsPage";


export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<Layout showSearchInHeader={true} />}>
          <Route path={PAGES.PUBLIC.HOME} element={<HomePage />} />
          <Route path={PAGES.PUBLIC.EVENTS} element={<EventsPage />} />
        </Route>

        {/* Private Routes */}
        <Route element={<Layout showSearchInHeader={false} />}>
          <Route path="/events/:id" element={<h1>Detalhes do Evento</h1>} />
          <Route path={PAGES.PRIVATE.PROFILE} element={<h1>Minha Conta</h1>} />
          <Route path={PAGES.PRIVATE.TICKETS} element={<h1>Meus Ingressos</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}