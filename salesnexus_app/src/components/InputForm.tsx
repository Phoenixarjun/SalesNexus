"use client";

import { useState } from "react";
import { toast } from "react-toastify";
import { FaStore, FaBox, FaCalendarAlt, FaTag, FaSearch, FaGasPump, FaShoppingCart, FaExclamationTriangle } from "react-icons/fa";
import ResultDisplay from "./ResultDisplay";

// Data options
const FAMILY_OPTIONS = ['AUTOMOTIVE', 'BABY CARE', 'BEAUTY', 'BEVERAGES', 'BOOKS', 'BREAD/BAKERY', 'CELEBRATION', 'CLEANING', 'DAIRY', 'DELI', 'EGGS', 'FROZEN FOODS', 'GROCERY I', 'GROCERY II', 'HARDWARE', 'HOME AND KITCHEN I', 'HOME AND KITCHEN II', 'HOME APPLIANCES', 'HOME CARE', 'LADIESWEAR', 'LAWN AND GARDEN', 'LINGERIE', 'LIQUOR,WINE,BEER', 'MAGAZINES', 'MEATS', 'PERSONAL CARE', 'PET SUPPLIES', 'PLAYERS AND ELECTRONICS', 'POULTRY', 'PREPARED FOODS', 'PRODUCE', 'SCHOOL AND OFFICE SUPPLIES', 'SEAFOOD'];
const CITY_OPTIONS = ['Quito', 'Santo Domingo', 'Cayambe', 'Latacunga', 'Riobamba', 'Ibarra', 'Guaranda', 'Puyo', 'Ambato', 'Guayaquil', 'Salinas', 'Daule', 'Babahoyo', 'Quevedo', 'Playas', 'Libertad', 'Cuenca', 'Loja', 'Machala', 'Esmeraldas', 'Manta', 'El Carmen'];
const STATE_OPTIONS = ['Pichincha', 'Santo Domingo de los Tsachilas', 'Cotopaxi', 'Chimborazo', 'Imbabura', 'Bolivar', 'Pastaza', 'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja', 'El Oro', 'Esmeraldas', 'Manabi'];
const TYPE_X_OPTIONS = [
  { value: 'D', label: 'Supermarket' },
  { value: 'B', label: 'Grocery Store' },
  { value: 'C', label: 'Warehouse' },
  { value: 'E', label: 'Convenience Store' },
  { value: 'A', label: 'Department Store' }
];
const TYPE_Y_OPTIONS = ['Holiday', 'Regular Day', 'Additional', 'Transfer', 'Event', 'Bridge'];

interface FormData {
  date: string;
  family: string;
  state: string;
  city: string;
  type_x: string;
  type_y: string;
  onpromotion: number;
  dcoilwtico: number;
  transactions: number;
  store_nbr: number;
  cluster: number;
}

export default function InputForm() {
  const [formData, setFormData] = useState<FormData>({
    date: "",
    family: "",
    state: "",
    city: "",
    type_x: "",
    type_y: "Regular Day",
    onpromotion: 0,
    dcoilwtico: 50.0,
    transactions: 1000,
    store_nbr: 1,
    cluster: 1
  });
  const [result, setResult] = useState<{ status: string; predicted_sales: number } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const [familySearch, setFamilySearch] = useState("");
  const [citySearch, setCitySearch] = useState("");
  const [stateSearch, setStateSearch] = useState("");
  const [showFamilyDropdown, setShowFamilyDropdown] = useState(false);
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [showStateDropdown, setShowStateDropdown] = useState(false);

  const filteredFamilyOptions = FAMILY_OPTIONS.filter(option =>
    option.toLowerCase().includes(familySearch.toLowerCase())
  );
  const filteredCityOptions = CITY_OPTIONS.filter(option =>
    option.toLowerCase().includes(citySearch.toLowerCase())
  );
  const filteredStateOptions = STATE_OPTIONS.filter(option =>
    option.toLowerCase().includes(stateSearch.toLowerCase())
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setResult(null);

    if (!formData.date || !formData.family || !formData.state || !formData.city || !formData.type_x) {
      setError("Please fill all required fields");
      setIsLoading(false);
      return;
    }

    try {
      const payload = {
        ...formData,
        date: new Date(formData.date).toISOString().split('T')[0], 
        store_nbr: Number(formData.store_nbr),
        cluster: Number(formData.cluster),
        onpromotion: Number(formData.onpromotion),
        dcoilwtico: Number(formData.dcoilwtico),
        transactions: Number(formData.transactions)
      };

      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed");
      }

      setResult(data);

      if (data.status === "success") {
        const sales = data.predicted_sales;
        if (sales >= 5000) {
          toast.success(
            <div>
              <strong>🚀 High Demand Alert!</strong>
              <p>Stock up immediately - predicted sales ${sales.toFixed(2)}</p>
            </div>,
            { position: "top-right", autoClose: 5000 }
          );
        } else if (sales <= 500) {
          toast.warn(
            <div>
              <strong>⚠️ Low Demand Warning</strong>
              <p>Adjust inventory - predicted sales ${sales.toFixed(2)}</p>
            </div>,
            { position: "top-right", autoClose: 5000 }
          );
        } else {
          toast.info(
            <div>
              <strong>📊 Normal Demand</strong>
              <p>Predicted sales ${sales.toFixed(2)}</p>
            </div>,
            { position: "top-right", autoClose: 3000 }
          );
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unknown error occurred";
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <h2 className="text-2xl font-bold text-center mb-6 text-white">
          Sales Prediction
        </h2>

        {/* Store Info Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Store Number */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Store Number*</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaStore className="text-gray-400" />
              </div>
              <input
                type="number"
                name="store_nbr"
                value={formData.store_nbr}
                onChange={(e) => setFormData({...formData, store_nbr: Number(e.target.value)})}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                required
                min="1"
              />
            </div>
          </div>

          {/* Cluster */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Cluster*</label>
            <input
              type="number"
              name="cluster"
              value={formData.cluster}
              onChange={(e) => setFormData({...formData, cluster: Number(e.target.value)})}
              className="w-full pl-4 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
              min="1"
              max="20"
              required
            />
          </div>
        </div>

        {/* Location Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* State */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">State*</label>
            <div className="relative">
              <input
                type="text"
                value={formData.state || stateSearch}
                onChange={(e) => {
                  setStateSearch(e.target.value);
                  setShowStateDropdown(true);
                }}
                onFocus={() => setShowStateDropdown(true)}
                onBlur={() => setTimeout(() => setShowStateDropdown(false), 200)}
                placeholder="Search state..."
                className="w-full pl-4 pr-10 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <FaSearch className="text-gray-400" />
              </div>
              {showStateDropdown && (
                <div className="absolute z-10 mt-1 w-full max-h-60 overflow-auto bg-gray-800 border border-gray-700 rounded-lg shadow-lg">
                  {filteredStateOptions.map((state) => (
                    <div
                      key={state}
                      className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
                      onMouseDown={() => {
                        setFormData({...formData, state});
                        setStateSearch("");
                        setShowStateDropdown(false);
                      }}
                    >
                      {state}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* City */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">City*</label>
            <div className="relative">
              <input
                type="text"
                value={formData.city || citySearch}
                onChange={(e) => {
                  setCitySearch(e.target.value);
                  setShowCityDropdown(true);
                }}
                onFocus={() => setShowCityDropdown(true)}
                onBlur={() => setTimeout(() => setShowCityDropdown(false), 200)}
                placeholder="Search city..."
                className="w-full pl-4 pr-10 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <FaSearch className="text-gray-400" />
              </div>
              {showCityDropdown && (
                <div className="absolute z-10 mt-1 w-full max-h-60 overflow-auto bg-gray-800 border border-gray-700 rounded-lg shadow-lg">
                  {filteredCityOptions.map((city) => (
                    <div
                      key={city}
                      className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
                      onMouseDown={() => {
                        setFormData({...formData, city});
                        setCitySearch("");
                        setShowCityDropdown(false);
                      }}
                    >
                      {city}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Product Info Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Family */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Product Family*</label>
            <div className="relative">
              <input
                type="text"
                value={formData.family || familySearch}
                onChange={(e) => {
                  setFamilySearch(e.target.value);
                  setShowFamilyDropdown(true);
                }}
                onFocus={() => setShowFamilyDropdown(true)}
                onBlur={() => setTimeout(() => setShowFamilyDropdown(false), 200)}
                placeholder="Search product family..."
                className="w-full pl-4 pr-10 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                <FaSearch className="text-gray-400" />
              </div>
              {showFamilyDropdown && (
                <div className="absolute z-10 mt-1 w-full max-h-60 overflow-auto bg-gray-800 border border-gray-700 rounded-lg shadow-lg">
                  {filteredFamilyOptions.map((family) => (
                    <div
                      key={family}
                      className="px-4 py-2 hover:bg-gray-700 cursor-pointer"
                      onMouseDown={() => {
                        setFormData({...formData, family});
                        setFamilySearch("");
                        setShowFamilyDropdown(false);
                      }}
                    >
                      {family}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Date */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Date*</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaCalendarAlt className="text-gray-400" />
              </div>
              <input
                type="date"
                name="date"
                value={formData.date}
                onChange={(e) => setFormData({...formData, date: e.target.value})}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              />
            </div>
          </div>
        </div>

        {/* Store Type Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Store Type */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Store Type*</label>
            <div className="relative">
              <select
                name="type_x"
                value={formData.type_x}
                onChange={(e) => setFormData({...formData, type_x: e.target.value})}
                className="w-full pl-4 pr-10 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white appearance-none focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              >
                <option value="">Select store type</option>
                {TYPE_X_OPTIONS.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label} ({type.value})
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>

          {/* Day Type */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Day Type*</label>
            <div className="relative">
              <select
                name="type_y"
                value={formData.type_y}
                onChange={(e) => setFormData({...formData, type_y: e.target.value})}
                className="w-full pl-4 pr-10 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white appearance-none focus:outline-none focus:ring-2 focus:ring-green-500"
                required
              >
                {TYPE_Y_OPTIONS.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Metrics Row */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* On Promotion */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">On Promotion</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaTag className="text-gray-400" />
              </div>
              <input
                type="number"
                name="onpromotion"
                value={formData.onpromotion}
                onChange={(e) => setFormData({...formData, onpromotion: Number(e.target.value)})}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                min="0"
              />
            </div>
          </div>

          {/* Oil Price */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Oil Price</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaGasPump className="text-gray-400" />
              </div>
              <input
                type="number"
                name="dcoilwtico"
                value={formData.dcoilwtico}
                onChange={(e) => setFormData({...formData, dcoilwtico: Number(e.target.value)})}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                step="0.1"
                min="0"
              />
            </div>
          </div>

          {/* Transactions */}
          <div className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-1">Transactions</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FaShoppingCart className="text-gray-400" />
              </div>
              <input
                type="number"
                name="transactions"
                value={formData.transactions}
                onChange={(e) => setFormData({...formData, transactions: Number(e.target.value)})}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                min="0"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full mt-6 py-3 px-4 bg-gradient-to-r from-green-500 to-purple-600 text-white font-semibold rounded-lg shadow-md transition-all duration-300 ${
            isLoading ? "opacity-70 cursor-not-allowed" : "hover:from-green-600 hover:to-purple-700 transform hover:scale-105"
          } focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75`}
        >
          {isLoading ? "Predicting..." : "Predict Sales"}
        </button>
      </form>

      {/* Display results or errors */}
      {error && (
        <div className="mt-6 p-4 bg-red-900 border border-red-500 rounded-lg">
          <div className="flex items-center">
            <FaExclamationTriangle className="text-red-400 text-2xl mr-3" />
            <p className="text-white">{error}</p>
          </div>
        </div>
      )}

      {result && <ResultDisplay result={result} />}
    </div>
  );
}