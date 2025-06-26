import React, { ReactNode } from "react";

interface StepCardProps {
  icon: ReactNode;
  title: string;
  description: string;
}

export default function StepCard({ icon, title, description }: StepCardProps) {
  return (
    <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 hover:border-green-400 transition-all duration-300 hover:shadow-lg hover:-translate-y-2">
      <div className="flex flex-col items-center text-center">
        <div className="mb-4 p-3 bg-gray-900 rounded-full">
          {icon}
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
        <p className="text-gray-300">{description}</p>
      </div>
    </div>
  );
}