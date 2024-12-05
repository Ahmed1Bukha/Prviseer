import React from "react";
import Link from "next/link";

const Navbar = () => {
  return (
    <nav>
      <div className="flex items-center justify-between p-4">
        <Link href="/" className="text-2xl font-bold">
          Chatbot
        </Link>
        <div className="flex items-center space-x-4">
          <Link href="/about" className="text-blue-500">
            About
          </Link>
          <Link href="/contact" className="text-blue-500">
            Contact
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
