import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RAMate - Your RA Assistant",
  description: "AI-powered assistant for Resident Assistants at Colorado State University. Get instant answers from training documents and policies.",
  keywords: ["RA", "Resident Assistant", "CSU", "Colorado State University", "AI Assistant", "Training"],
  authors: [{ name: "RAMate Team" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
