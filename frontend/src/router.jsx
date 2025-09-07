import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Ana sayfalar
import MusteriPanel from './pages/musteri_panel/Musteri.jsx';
import IsletmePanel from './pages/isletme_panel/Isletme.jsx';
import OdemeAdimlari from './pages/odeme_adimlari/Odeme.jsx';
import IsletmeDynamic from './pages/IsletmeDynamic.jsx';

// Müşteri panel alt sayfaları
import RandevuAl from './pages/musteri_panel/randevu_al/RandevuAl.jsx';
import Galeri from './pages/musteri_panel/galeri/Galeri.jsx';
import SSS from './pages/musteri_panel/sss/SSS.jsx';
import Iletisim from './pages/musteri_panel/iletisim/Iletisim.jsx';

// İşletme panel alt sayfaları
import Anasayfa from './pages/isletme_panel/anasayfa/Anasayfa.jsx';
import Personel from './pages/isletme_panel/personel/Personel.jsx';
import GenelAyarlar from './pages/isletme_panel/ayarlar/genel_ayarlar/GenelAyarlar.jsx';
import RandevuAyarlar from './pages/isletme_panel/ayarlar/randevu_ayarlari/RandevuAyarlari.jsx';
import GaleriAyarlar from './pages/isletme_panel/ayarlar/galeri_ayarlari/GaleriAyarlari.jsx';
import IletisimAyarlar from './pages/isletme_panel/ayarlar/iletisim_ayarlari/IletisimAyarlari.jsx';
import SSSEkle from './pages/isletme_panel/ayarlar/sss_ayarlari/SssAyarlari.jsx'; 

// Ödeme adımları alt sayfaları
import HizmetDetaylari from './pages/odeme_adimlari/hizmet_detaylari/HizmetDetaylari.jsx';
import MusteriBilgileri from './pages/odeme_adimlari/musteri_bilgileri/MusteriBilgileri.jsx';
import OnIzleme from './pages/odeme_adimlari/on_izleme/OnIzleme.jsx';
import TarihSaat from './pages/odeme_adimlari/tarih_saat/TarihSaat.jsx';

export default function AppRouter() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/musteri" />} />
        <Route path="/musteri" element={<MusteriPanel />} />
        <Route path="/isletme" element={<IsletmePanel />} />
        <Route path="/odeme" element={<OdemeAdimlari />} />

        {/* Müşteri Panel Alt Sayfaları */}
        <Route path="/musteri/randevu-al" element={<RandevuAl />} />
        <Route path="/musteri/galeri" element={<Galeri />} />
        <Route path="/musteri/sss" element={<SSS />} />
        <Route path="/musteri/iletisim" element={<Iletisim />} />

        {/* İşletme Panel Alt Sayfaları */}
        <Route path="/isletme/anasayfa" element={<Anasayfa />} />
        <Route path="/isletme/personel" element={<Personel />} />
        <Route path="/isletme/ayarlar/genel" element={<GenelAyarlar />} />
        <Route path="/isletme/ayarlar/randevu" element={<RandevuAyarlar />} />
        <Route path="/isletme/ayarlar/galeri" element={<GaleriAyarlar />} />
        <Route path="/isletme/ayarlar/iletisim" element={<IletisimAyarlar />} />
        <Route path="/isletme/ayarlar/sss" element={<SSSEkle />} /> 

        {/* Ödeme Alt Sayfaları */}
        <Route path="/odeme/hizmet" element={<HizmetDetaylari />} />
        <Route path="/odeme/musteri" element={<MusteriBilgileri />} />
        <Route path="/odeme/onizleme" element={<OnIzleme />} />
        <Route path="/odeme/tarih-saat" element={<TarihSaat />} />

        {/* Dinamik işletme sayfaları */}
        <Route path="/:isletmeSlug" element={<IsletmeDynamic page="anasayfa" />} />
        <Route path="/:isletmeSlug/randevu" element={<IsletmeDynamic page="randevu" />} />

      </Routes>
    </Router>
  );
}
