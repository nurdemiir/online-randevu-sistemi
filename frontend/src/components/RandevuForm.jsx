
import { useState } from 'react';
import { postRandevu } from '../services/api';

export default function RandevuForm() {
    const [ad, setAd] = useState('');
    const [soyad, setSoyad] = useState('');
    const [mesaj, setMesaj] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await postRandevu({ ad, soyad });
        setMesaj(response.mesaj);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Adınız" value={ad} onChange={e => setAd(e.target.value)} required />
            <input type="text" placeholder="Soyadınız" value={soyad} onChange={e => setSoyad(e.target.value)} required />
            <button type="submit">Randevu Al</button>
            {mesaj && <p>{mesaj}</p>}
        </form>
    );
}
