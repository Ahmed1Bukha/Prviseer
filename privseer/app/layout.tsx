import type { Metadata } from "next";

import "./globals.css";
import Navbar from "./Navbar";

export const metadata: Metadata = {
  title: "Privseer",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="h-screen">
        <div className="flex flex-col h-full">
          {/* <Navbar /> */}

          {/* Main content with adjusted top padding and height */}
          <main className="flex-1 pt-16">{children}</main>
        </div>
      </body>
    </html>
  );
}
