import React, { ReactNode } from "react";

interface SectionProps {
  id: string;
  children: ReactNode;
  className?: string;
}

export default function Section({ id, children, className = "" }: SectionProps) {
  return (
    <section id={id} className={`${className} scroll-mt-20`}>
      {children}
    </section>
  );
}