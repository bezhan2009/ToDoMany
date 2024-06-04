import { useState, useRef, useEffect } from "react";

function useCustomIntersectionObserver() {
  const [elementIsVisible, setElementVisible] = useState(false);
  const targetRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      setElementVisible(entry.isIntersecting);
    });

    if (targetRef.current) {
      observer.observe(targetRef.current);
    }

    return () => {
      if (targetRef.current) {
        observer.unobserve(targetRef.current);
      }
    };
  }, []);

  return { targetRef, elementIsVisible };
}

export default useCustomIntersectionObserver;
