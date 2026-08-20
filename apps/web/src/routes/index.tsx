import { BrowserRouter, Route, Routes } from "react-router-dom";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<h1>Hero</h1>} />
        <Route path="/events" element={<h1>Eventos</h1>} />
        <Route path="/events/:id" element={<h1>Pagina de evento</h1>} />
      </Routes>
    </BrowserRouter>
  )
}