import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";

/**
 * @Usage
 *  const { t, i18n } = useTranslation();
 *   i18n.changeLanguage('en');
 * {t('Sample text')}
 */

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    // we init with resources
    resources: {
      en: {
        translations: {
          "Sample text": "Some translation in English",
        },
      },
      ja: {
        translations: {
          "Sample text": "Some translation in Japanese",
        },
      },
    },
    fallbackLng: "en",
    debug: process.env.NODE_ENV === "development",
    ns: ["translations"],
    defaultNS: "translations",

    keySeparator: false, // we use content as keys

    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
