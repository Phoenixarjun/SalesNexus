"use client";

import { useState } from "react";
import { FaExclamationTriangle, FaThumbsUp, FaThumbsDown } from "react-icons/fa";

export default function ResultDisplay() {
  const [result, setResult] = useState<{
    status: "success" | "error" | null;
    message: string;
    sales: number | null;
  }>({ status: null, message: "", sales: null });

  // Mock prediction function
  const handlePredict = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate API call
    setTimeout(() => {
      const random = Math.random();
      if (random > 0.1) { // 90% chance of success
        const sales = Math.floor(Math.random() * 10000);
        setResult({
          status: "success",
          sales,
          message: sales > 5000 
            ? "High Demand! Increase your stock ⚡️" 
            : "Low Demand. Optimize your inventory 👇",
        });
      } else {
        setResult({
          status: "error",
          sales: null,
          message: "Failed to get prediction. Please try again later.",
        });
      }
    }, 1500);
  };

  if (result.status === null) return null;

  return (
    <div
      className={`mt-6 p-4 rounded-lg transition-all duration-500 ease-in-out ${
        result.status === "success"
          ? "bg-gray-800 border border-green-500"
          : "bg-red-900 border border-red-500"
      }`}
    >
      {result.status === "error" ? (
        <div className="flex items-center">
          <FaExclamationTriangle className="text-red-400 text-2xl mr-3" />
          <p className="text-white">{result.message}</p>
        </div>
      ) : (
        <div>
          <div className="flex items-center mb-2">
            {result.sales && result.sales > 5000 ? (
              <FaThumbsUp className="text-green-400 text-2xl mr-3" />
            ) : (
              <FaThumbsDown className="text-yellow-400 text-2xl mr-3" />
            )}
            <h3 className="text-xl font-semibold text-white">Prediction Result</h3>
          </div>
          <p className="text-gray-300 mb-1">Estimated Sales: <span className="font-bold text-white">{result.sales?.toLocaleString()}</span></p>
          <p className="text-gray-300">{result.message}</p>
        </div>
      )}
    </div>
  );
}