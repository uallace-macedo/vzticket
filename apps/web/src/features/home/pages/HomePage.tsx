import { HeroSection } from "../components/HeroSection"
import { StatsBanner } from "../components/StatsBanner"
import { FeaturesGrid } from "../components/FeaturesGrid"

export function HomePage() {
  return (
    <div className="space-y-12 pb-12">
      <HeroSection />
      <StatsBanner />
      <FeaturesGrid />
    </div>
  )
}