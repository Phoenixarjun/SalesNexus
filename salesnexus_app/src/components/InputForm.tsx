"use client";

import { useState } from "react";
import { FaStore, FaBox, FaCalendarAlt, FaTag } from "react-icons/fa";

export default function InputForm() {
  const [formData, setFormData] = useState({
    storeId: "",
    itemId: "",
    date: "",
    promotion: "none",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  return (
    <form className="space-y-6">
      <h2 className="text-2xl font-bold text-center mb-6 text-white">
        Sales Prediction
      </h2>
      
      <div className="space-y-4">
        {/* Store ID */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaStore className="text-gray-400" />
          </div>
          <input
            type="text"
            name="storeId"
            value={formData.storeId}
            onChange={handleChange}
            placeholder="Store ID"
            className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Item ID */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaBox className="text-gray-400" />
          </div>
          <input
            type="text"
            name="itemId"
            value={formData.itemId}
            onChange={handleChange}
            placeholder="Item ID"
            className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Date */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaCalendarAlt className="text-gray-400" />
          </div>
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500"
            required
          />
        </div>

        {/* Promotion */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <FaTag className="text-gray-400" />
          </div>
          <select
            name="promotion"
            value={formData.promotion}
            onChange={handleChange}
            className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white appearance-none focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="none">No Promotion</option>
            <option value="low">Low Promotion</option>
            <option value="high">High Promotion</option>
          </select>
          <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
            <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
      </div>

      <button
        type="submit"
        className="w-full py-3 px-4 bg-gradient-to-r from-green-500 to-purple-600 hover:from-green-600 hover:to-purple-700 text-white font-semibold rounded-lg shadow-md transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
      >
        Predict Sales
      </button>
    </form>
  );
}