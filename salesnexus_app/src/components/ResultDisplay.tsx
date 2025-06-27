"use client";

import { FaExclamationTriangle, FaFire, FaChartLine, FaBoxOpen } from "react-icons/fa";

interface ResultDisplayProps {
  result: {
    status: string;
    predicted_sales: number;
    message?: string;
  };
}

const SALES_THRESHOLDS = {
  HIGH: 5000,    
  LOW: 500      
};

export default function ResultDisplay({ result }: ResultDisplayProps) {
  if (!result || result.status === "") return null;

  const sales = result.predicted_sales;
  const isHighDemand = sales >= SALES_THRESHOLDS.HIGH;
  const isLowDemand = sales <= SALES_THRESHOLDS.LOW;

  const getDemandLevel = () => {
    if (isHighDemand) return "High Demand";
    if (isLowDemand) return "Low Demand";
    return "Normal Demand";
  };

  const getRecommendation = () => {
    if (isHighDemand) return "Increase inventory and schedule extra staff";
    if (isLowDemand) return "Reduce orders and consider promotions";
    return "Maintain current stock levels";
  };

  const getIcon = () => {
    if (isHighDemand) return <FaFire className="text-red-500 text-3xl" />;
    if (isLowDemand) return <FaBoxOpen className="text-yellow-500 text-3xl" />;
    return <FaChartLine className="text-green-500 text-3xl" />;
  };

  const getCardColor = () => {
    if (isHighDemand) return "bg-gradient-to-br from-red-900/50 to-red-800/80";
    if (isLowDemand) return "bg-gradient-to-br from-yellow-900/50 to-yellow-800/80";
    return "bg-gradient-to-br from-green-900/50 to-green-800/80";
  };

  return (
    <div className="mt-6">
      {result.status !== "success" ? (
        <div className="p-4 bg-red-900/80 border border-red-500 rounded-lg flex items-center">
          <FaExclamationTriangle className="text-red-300 text-2xl mr-3" />
          <p className="text-white">{result.message || "Prediction failed"}</p>
        </div>
      ) : (
        <div className={`p-6 rounded-lg shadow-lg ${getCardColor()} border border-gray-600`}>
          <div className="flex items-start space-x-4">
            <div className="mt-1">{getIcon()}</div>
            <div className="flex-1">
              <div className="flex justify-between items-start">
                <h3 className="text-xl font-bold text-white">Sales Prediction</h3>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  isHighDemand ? "bg-red-500/90" : isLowDemand ? "bg-yellow-500/90" : "bg-green-500/90"
                }`}>
                  {getDemandLevel()}
                </span>
              </div>
              
              <div className="mt-4">
                <p className="text-gray-300 text-sm">Estimated Sales</p>
                <p className="text-3xl font-bold text-white">${sales.toFixed(2)}</p>
              </div>
              
              <div className="mt-4 p-3 bg-black/30 rounded-lg">
                <p className="text-sm text-gray-200 font-medium">Recommendation</p>
                <p className="text-white">{getRecommendation()}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}