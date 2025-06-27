import React, { ReactNode } from "react";

interface StepCardProps {
  icon: ReactNode;
  title: string;
  description: string;
  gradient?: string;
}

export default function StepCard({ icon, title, description, gradient }: StepCardProps) {
  return (
    <div className={`p-6 rounded-xl border border-gray-200 hover:border-green-400 transition-all duration-300 hover:shadow-lg hover:-translate-y-2 ${
      gradient ? `bg-gradient-to-br ${gradient}` : 'bg-gray-800'
    } shadow-[0_8px_30px_rgba(255,255,255,0.1)] hover:shadow-[0_8px_30px_rgba(255,255,255,0.2)]`}>
      <div className="flex flex-col items-center text-center h-full">
        <div className={`mb-4 p-3 rounded-full ${
          gradient ? 'bg-black/30' : 'bg-gray-900'
        }`}>
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
        <p className="text-gray-300">{description}</p>
      </div>
    </div>
  );
}