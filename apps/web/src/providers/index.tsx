import { QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { queryClient } from "../lib/react-query";
import { Toaster } from "sonner";

interface AppProviderProps {
  children: ReactNode
}

export function AppProvider(props: AppProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {props.children}
      <Toaster position="top-right" richColors duration={1500} />
    </QueryClientProvider>
  )
}