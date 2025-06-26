import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import InputForm from "@/components/InputForm";
import ResultDisplay from "@/components/ResultDisplay";
import Section from "@/components/Section";
import StepCard from "@/components/StepCard";
import { FaIdCard, FaCalendarAlt, FaChartLine, FaLightbulb } from "react-icons/fa";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <Navbar />
      
      <main className="container mx-auto px-4">
        {/* Landing Section */}
        <Section id="home" className="min-h-screen pt-32 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-purple-500 mb-6">
                Forecast Sales Like Never Before
              </h1>
              <p className="text-xl text-gray-300 mb-8">
                Leverage AI-powered predictions to optimize your inventory and maximize profits.
              </p>
            </div>
            <div className="bg-gray-800 p-8 rounded-xl shadow-2xl border border-gray-700">
              <InputForm />
              <ResultDisplay />
            </div>
          </div>
        </Section>

        {/* About Section */}
        <Section id="about" className="py-20">
          <div className="bg-gray-800 p-8 md:p-12 rounded-xl shadow-xl border border-gray-700">
            <h2 className="text-3xl font-bold text-center mb-12 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-purple-500">
              About SalesNexus
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
                <h3 className="text-xl font-semibold mb-3 text-green-400">What is SalesNexus?</h3>
                <p className="text-gray-300">
                  An AI-powered sales forecasting tool that helps retailers predict demand with unprecedented accuracy.
                </p>
              </div>
              <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
                <h3 className="text-xl font-semibold mb-3 text-purple-400">Why It's Needed</h3>
                <p className="text-gray-300">
                  Reduce waste, optimize stock levels, and never miss sales opportunities due to stockouts.
                </p>
              </div>
              <div className="bg-gray-900 p-6 rounded-lg border border-gray-700">
                <h3 className="text-xl font-semibold mb-3 text-green-400">The Impact</h3>
                <p className="text-gray-300">
                  Better forecasting leads to higher sales, lower costs, and improved customer satisfaction.
                </p>
              </div>
            </div>
          </div>
        </Section>

        {/* Guide Section */}
        <Section id="guide" className="py-20">
          <h2 className="text-3xl font-bold text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-green-500">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StepCard 
              icon={<FaIdCard className="text-4xl text-green-400" />}
              title="Enter Details"
              description="Provide your Store ID, Item ID, Date, and Promotion status."
            />
            <StepCard 
              icon={<FaCalendarAlt className="text-4xl text-purple-400" />}
              title="Click Predict"
              description="Our AI analyzes historical data and market trends."
            />
            <StepCard 
              icon={<FaChartLine className="text-4xl text-green-400" />}
              title="Get Insights"
              description="Receive accurate sales predictions with actionable recommendations."
            />
          </div>
        </Section>
      </main>

      <Footer />
    </div>
  );
}