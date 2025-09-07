import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

export default function IsletmeDynamic({ page }) {
  const { isletmeSlug } = useParams();
  const [isletme, setIsletme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`/api/genel-ayarlar/liste?slug=${isletmeSlug}`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          setIsletme(data[0]);
        } else if (data.slug) {
          setIsletme(data);
        } else {
          setError('İşletme bulunamadı');
        }
        setLoading(false);
      })
      .catch(() => {
        setError('Sunucu hatası');
        setLoading(false);
      });
  }, [isletmeSlug]);

  if (loading) return <div>Yükleniyor...</div>;
  if (error) return <div>{error}</div>;
  if (!isletme) return <div>İşletme bulunamadı</div>;

  if (page === 'anasayfa') {
    return (
      <div>
        <h1>{isletme.isletme_adi}</h1>
        <p>{isletme.aciklama}</p>
        {isletme.logo && <img src={isletme.logo} alt="Logo" width={200} />}
        <p>Açılış: {isletme.acilis_saati} - Kapanış: {isletme.kapanis_saati}</p>
        <a href={`/${isletme.slug}/randevu`}>Randevu Al</a>
      </div>
    );
  }
  if (page === 'randevu') {
    return (
      <div>
        <h1>{isletme.isletme_adi} - Randevu Al</h1>
        <p>Buraya randevu formu ve işletmeye özel bilgiler gelecek.</p>
        <a href={`/${isletme.slug}`}>Anasayfa</a>
      </div>
    );
  }
  return <div>Sayfa bulunamadı</div>;
} 