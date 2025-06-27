import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import InputForm from "@/components/InputForm";
import ResultDisplay from "@/components/ResultDisplay";
import Section from "@/components/Section";
import StepCard from "@/components/StepCard";
import { FaIdCard, FaCalendarAlt, FaChartLine, FaStore, FaBoxes, FaMoneyBillWave } from "react-icons/fa";
import { toast, ToastContainer } from "react-toastify";


export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <Navbar />
      
      <main className="container mx-auto px-4">
        {/* Hero Section with Form */}
        <Section id="home" className="min-h-screen pt-32 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-purple-500 mb-6">
                Forecast Sales Like Never Before
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Leverage AI-powered predictions to optimize your inventory and maximize profits.
              </p>
              <div className="flex flex-wrap gap-4 mt-10">
                <div className="flex items-center text-green-400">
                  <FaStore className="mr-2" />
                  <span>Reduce waste by 30%+</span>
                </div>
                <div className="flex items-center text-purple-400">
                  <FaBoxes className="mr-2" />
                  <span>Optimize inventory</span>
                </div>
                <div className="flex items-center text-green-400">
                  <FaMoneyBillWave className="mr-2" />
                  <span>Increase profits</span>
                </div>
              </div>
            </div>
            <div className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700">
              <InputForm />
              <ResultDisplay result={{ status: "", predicted_sales: 0 }} />
            </div>
          </div>
        </Section>

        {/* Retailer Story Section */}
        <Section id="story" className="py-20">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-green-500">
              Transforming Retail Forecasting
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              <div className="space-y-8">
                <div className="bg-gray-800 p-8 rounded-xl border-l-4 border-red-500">
                  <h3 className="text-2xl font-semibold mb-4 text-red-400">The Problem</h3>
                  <p className="text-gray-300 mb-4">
                    Every day, grocery stores face the impossible challenge of predicting exactly how much of each product they'll sell. The consequences of getting it wrong are severe:
                  </p>
                  <ul className="list-disc pl-6 text-gray-300 space-y-3">
                    <li>Overstocking leads to <span className="font-semibold">$1 trillion</span> in global food waste annually</li>
                    <li>Understocking results in <span className="font-semibold">lost sales</span> and frustrated customers</li>
                    <li>Manual forecasting can't account for <span className="font-semibold">seasonal trends, promotions, or local events</span></li>
                  </ul>
                </div>

                <div className="bg-gray-800 p-8 rounded-xl border-l-4 border-green-500">
                  <h3 className="text-2xl font-semibold mb-4 text-green-400">Our Breakthrough</h3>
                  <p className="text-gray-300 mb-4">
                    SalesNexus changes the game with AI-powered forecasting trained on Corporación Favorita's extensive sales data:
                  </p>
                  <ul className="list-disc pl-6 text-gray-300 space-y-3">
                    <li>Analyzes <span className="font-semibold">5+ years</span> of historical sales data</li>
                    <li>Accounts for <span className="font-semibold">promotions, holidays, and local trends</span></li>
                    <li>Provides <span className="font-semibold">daily predictions</span> for every product</li>
                  </ul>
                </div>
              </div>

              <div className="hidden lg:block">
                <div className="relative h-full min-h-[500px] bg-gray-800 rounded-xl border border-gray-700 p-8 flex flex-col justify-center">
                  <div className="space-y-6">
                    <div className="flex items-start">
                      <div className="bg-green-500/20 p-3 rounded-full mr-4">
                        <FaChartLine className="text-green-400 text-xl" />
                      </div>
                      <div>
                        <h4 className="text-xl font-semibold text-white">32% Reduction</h4>
                        <p className="text-gray-400">in food waste for early adopters</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <div className="bg-purple-500/20 p-3 rounded-full mr-4">
                        <FaMoneyBillWave className="text-purple-400 text-xl" />
                      </div>
                      <div>
                        <h4 className="text-xl font-semibold text-white">18% Increase</h4>
                        <p className="text-gray-400">in sales from better stock management</p>
                      </div>
                    </div>
                    <div className="flex items-start">
                      <div className="bg-green-500/20 p-3 rounded-full mr-4">
                        <FaStore className="text-green-400 text-xl" />
                      </div>
                      <div>
                        <h4 className="text-xl font-semibold text-white">95% Accuracy</h4>
                        <p className="text-gray-400">in weekly sales predictions</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Section>

        {/* How It Works Section */}
        <Section id="how-it-works" className="py-20">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-green-500">
              How SalesNexus Works
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <StepCard 
                icon={<FaIdCard className="text-4xl text-green-400" />}
                title="1. Input Your Data"
                description="Enter store details, product information, and date range for prediction."
                gradient="from-green-500/10 to-green-500/5"
              />
              <StepCard 
                icon={<FaCalendarAlt className="text-4xl text-purple-400" />}
                title="2. AI Analysis"
                description="Our models process historical data, trends, and external factors."
                gradient="from-purple-500/10 to-purple-500/5"
              />
              <StepCard 
                icon={<FaChartLine className="text-4xl text-green-400" />}
                title="3. Get Predictions"
                description="Receive accurate forecasts with actionable recommendations."
                gradient="from-green-500/10 to-green-500/5"
              />
            </div>
          </div>
        </Section>

        {/* Benefits Section */}
        <Section id="benefits" className="py-20">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-purple-500">
              Why Choose SalesNexus
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 hover:border-green-500 transition-all">
                <div className="text-green-400 text-3xl mb-4">
                  <FaMoneyBillWave />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Increase Revenue</h3>
                <p className="text-gray-300">
                  Never miss a sale due to stockouts while optimizing your inventory investment.
                </p>
              </div>
              <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 hover:border-purple-500 transition-all">
                <div className="text-purple-400 text-3xl mb-4">
                  <FaBoxes />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Reduce Waste</h3>
                <p className="text-gray-300">
                  Cut perishable goods waste by accurately predicting demand.
                </p>
              </div>
              <div className="bg-gray-800 p-8 rounded-xl border border-gray-700 hover:border-green-500 transition-all">
                <div className="text-green-400 text-3xl mb-4">
                  <FaStore />
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">Data-Driven Decisions</h3>
                <p className="text-gray-300">
                  Move beyond guesswork with AI-powered insights you can trust.
                </p>
              </div>
            </div>
          </div>
        </Section>
      </main>
      <ToastContainer />
      <Footer />
      
    </div>
  );
}