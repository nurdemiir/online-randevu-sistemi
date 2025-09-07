
export const postRandevu = async (veri) => {
    const res = await fetch("/api/randevu-al", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(veri)
    });
    return res.json();
};
