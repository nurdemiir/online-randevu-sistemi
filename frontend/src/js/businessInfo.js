// frontend/src/js/businessInfo.js

// İşletme bilgilerini yükleyen fonksiyon
async function loadBusinessInfo() {
    try {
        // Tüm GenelAyar kayıtlarını çek
        const response = await fetch('http://localhost:8000/api/genel-ayarlar/liste');
        const ayarlar = await response.json();

        if (ayarlar.length === 0) return;
        const ayar = ayarlar[0]; // En güncel ayarı al

        const h1Element = document.getElementById('sidebar-h1');
        const h2Element = document.getElementById('sidebar-h2');
        const imgElement = document.getElementById('business-image');

        if (h1Element) h1Element.textContent = ayar.isletme_adi || 'Varsayılan İşletme';
        if (h2Element) h2Element.textContent = ayar.aciklama || 'Panel';

        if (imgElement) {
            if (ayar.logo) {
                imgElement.src = 'http://localhost:8000' + ayar.logo + '?v=' + Date.now(); // Cache kırıcı
            } else {
                imgElement.src = '/frontend/public/assets/blank-white.png'; // Yedek beyaz resim yolu
            }
        }

        // isletme_adi değerini localStorage'a kaydet (galeri API için)
        localStorage.setItem('isletme_adi', ayar.isletme_adi || 'Varsayılan İşletme');
    } catch (error) {
        console.error('İşletme bilgileri yüklenirken hata:', error);
    }
}

// isletme_adi değerini almak için yardımcı fonksiyon
function getIsletmeAdi() {
    return localStorage.getItem('isletme_adi') || 'Varsayılan İşletme';
}