import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "../components/Layout";
import { HomePage } from "@/features/home/pages/HomePage";


export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route element={<Layout showSearchInHeader={true} />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/events" element={<h1>Lista de Eventos</h1>} />
          <Route path="/account" element={<h1>Minha Conta</h1>} />
          <Route path="/tickets" element={<h1>Meus Ingressos</h1>} />
        </Route>

        <Route element={<Layout showSearchInHeader={false} />}>
          <Route path="/events/:id" element={<h1>Detalhes do Evento</h1>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}