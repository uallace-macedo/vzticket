import { Outlet } from 'react-router-dom'
import { Header } from './Header'
import { Footer } from './Footer'

interface LayoutProps {
  showSearchInHeader?: boolean
}

export function Layout({ showSearchInHeader = true }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background flex flex-col justify-between">
      <Header showSearch={showSearchInHeader} />
      <main className="flex-1">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}