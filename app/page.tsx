import Calculator from "@/components/Calculator";
import CurrentLine from "@/components/CurrentLine";
import CutMoment from "@/components/CutMoment";
import DayTimeline from "@/components/DayTimeline";
import Faq from "@/components/Faq";
import FinalCta from "@/components/FinalCta";
import Footer from "@/components/Footer";
import FourPrices from "@/components/FourPrices";
import Hero from "@/components/Hero";
import HowItStarts from "@/components/HowItStarts";
import Nav from "@/components/Nav";
import Offerings from "@/components/Offerings";
import Software from "@/components/Software";
import WhoShouldnt from "@/components/WhoShouldnt";

export default function Home() {
  return (
    <>
      <Nav />
      <main className="relative overflow-x-clip">
        <CurrentLine />
        <Hero />
        <div data-station>
          <FourPrices />
        </div>
        <div data-station>
          <CutMoment />
        </div>
        <div data-station>
          <DayTimeline />
        </div>
        <div data-station>
          <Calculator />
        </div>
        <div data-station>
          <Offerings />
        </div>
        <div data-station>
          <Software />
        </div>
        <div data-station>
          <HowItStarts />
        </div>
        <div data-station>
          <WhoShouldnt />
        </div>
        <div data-station>
          <Faq />
        </div>
        <FinalCta />
      </main>
      <Footer />
    </>
  );
}
