import Link from "next/link";
import Logo from "../../public/logo.png"; 
import Image from "next/image";

export default function Footer() {
  return (
    <footer className="bg-gray-900 border-t border-gray-800 px-4">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-center">
          {/* Logo */}
            <Link href="#home" className="flex items-center">
              <Image
                src={Logo}
                alt="SalesNexus Logo"
                width={150}
                height={150}
                className="rounded-full"
              />
            </Link>

          {/* Links */}
          <div className="flex justify-center space-x-6">
            <Link
              href="#"
              className="text-gray-400 hover:text-green-400 transition-colors duration-300"
            >
              Privacy Policy
            </Link>
            <Link
              href="#"
              className="text-gray-400 hover:text-green-400 transition-colors duration-300"
            >
              Terms of Service
            </Link>
          </div>

          {/* Copyright */}
          <div className="text-gray-400 text-sm text-center md:text-right">
            © 2025 Created by Naresh B A
          </div>
        </div>
      </div>
    </footer>
  );
}