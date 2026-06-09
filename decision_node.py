from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DecisionNode:
    """Restoran karar ağacındaki bir düğümü temsil eder."""

    name: str
    children: dict[str, DecisionNode] = field(default_factory=dict)

    def add_child(self, branch_name: str, child: DecisionNode) -> None:
        """Düğüme yeni bir alt dal ekler."""
        if not branch_name:
            raise ValueError("Dal adı boş olamaz.")
        if branch_name in self.children:
            raise ValueError(f"'{branch_name}' dalı zaten mevcut.")

        self.children[branch_name] = child

    def get_child(self, branch_name: str) -> DecisionNode | None:
        """Dal adına göre alt düğümü döndürür."""
        return self.children.get(branch_name)

    def remove_child(self, branch_name: str) -> DecisionNode | None:
        """Dalı siler ve silinen düğümü döndürür."""
        return self.children.pop(branch_name, None)

    def is_leaf(self) -> bool:
        """Alt dalı olmayan düğümleri belirler."""
        return not self.children


def build_restaurant_tree() -> DecisionNode:
    """Genişletilmiş restoran ağacını oluşturur ve kök düğümü döndürür."""
    
    root = DecisionNode("Restoran Sistemi")

    customer = DecisionNode("Müşteri İşlemleri Ana Menüsü")
    staff = DecisionNode("Personel İşlemleri Ana Menüsü")
    menu = DecisionNode("Menü Yönetimi Ana Menüsü")

    root.add_child("müşteri", customer)
    root.add_child("personel", staff)
    root.add_child("menü", menu)

    c_rezervasyon = DecisionNode("Müşteri Rezervasyon İşlemleri")
    c_siparis = DecisionNode("Müşteri Sipariş Türleri")
    c_odeme = DecisionNode("Müşteri Ödeme Yöntemleri")

    customer.add_child("rezervasyon", c_rezervasyon)
    customer.add_child("sipariş", c_siparis)
    customer.add_child("ödeme", c_odeme)

    c_rezervasyon.add_child("masa", DecisionNode("Masa Rezervasyon Ekranı"))
    c_rezervasyon.add_child("etkinlik", DecisionNode("Toplu Etkinlik/Organizasyon Planlama Ekranı"))
    
    c_siparis.add_child("masadan", DecisionNode("Masadan Sipariş Verici Giriş Ekranı"))
    c_siparis.add_child("paket", DecisionNode("Paket Servis ve Gel-Al Takip Sistemi"))
    
    c_odeme.add_child("nakit_kart", DecisionNode("Nakit veya Kredi Kartı Tahsilat Ekranı"))
    c_odeme.add_child("qr", DecisionNode("QR Kod ile Temassız Ödeme Modülü"))

    s_garson = DecisionNode("Garson Panel Seçenekleri")
    s_mutfak = DecisionNode("Mutfak Yönetim Paneli")
    s_yonetici = DecisionNode("Yönetici Yetki Alanı")

    staff.add_child("garson", s_garson)
    staff.add_child("mutfak", s_mutfak)
    staff.add_child("yönetici", s_yonetici)

    s_garson.add_child("masa_takip", DecisionNode("Masaların Doluluk ve Sipariş Durum Matrisi"))
    s_garson.add_child("siparis_ilet", DecisionNode("Yeni Siparişi Mutfağa Gönderme Terminali"))
    
    s_mutfak.add_child("hazırlama", DecisionNode("Sıradaki Hazırlanacak Yemekler Kuyruğu (Queue)"))
    s_mutfak.add_child("stok", DecisionNode("Kritik Stok Seviyesi ve Depo Kontrol Ekranı"))
    
    s_yonetici.add_child("rapor", DecisionNode("Günlük/Aylık Ciro Raporları Analiz Ekranı"))
    s_yonetici.add_child("mesai", DecisionNode("Personel Vardiya ve İzin Düzenleme Tablosu"))

    m_yemekler = DecisionNode("Yemek Kategorileri")
    m_icecekler = DecisionNode("İçecek Kategorileri")
    m_tatlilar = DecisionNode("Tatlı Kategorileri")

    menu.add_child("yemekler", m_yemekler)
    menu.add_child("içecekler", m_icecekler)
    menu.add_child("tatlılar", m_tatlilar)

    m_yemekler.add_child("çorbalar", DecisionNode("Günün Çorbaları ve Başlangıçlar Listesi"))
    m_yemekler.add_child("ana_yemekler", DecisionNode("Izgaralar, Tavalar ve Ev Yemekleri Listesi"))
    m_yemekler.add_child("salatalar", DecisionNode("Diyet ve Yan Salata Çeşitleri Listesi"))
    
    m_icecekler.add_child("sıcak_içecekler", DecisionNode("Çay, Kahve ve Bitki Çayları Menüsü"))
    m_icecekler.add_child("soğuk_içecekler", DecisionNode("Meşrubatlar, Taze Sıkılmış Meyve Suları Menüsü"))
    
    m_tatlilar.add_child("şerbetli_tatlılar", DecisionNode("Baklava, Kadayıf ve Künefe Seçenekleri"))
    m_tatlilar.add_child("sütlü_tatlılar", DecisionNode("Sütlaç, Kazandibi ve Magnolia Seçenekleri"))

    return root

def traverse(current_node: DecisionNode) -> None:
    """Kullanıcının seçimlerine göre genişletilmiş ağaçta dinamik olarak gezinir."""
    
    if current_node.is_leaf():
        print(f"\n[SİSTEM] Başarıyla yönlendirildiniz: {current_node.name}")
        return

    print(f"\n--- {current_node.name} ---")
    print("İlerlemek istediğiniz seçeneği tam olarak yazın:")
    
    for branch_name in current_node.children.keys():
        print(f" > {branch_name}")

    choice = input("Seçiminiz: ").strip().lower()

    next_node = current_node.get_child(choice)

    if next_node is not None:
        traverse(next_node)
    else:
        print(f"\nHata: '{choice}' geçerli bir menü seçeneği değil. Lütfen tekrar deneyin.")
        traverse(current_node)

restaurant_root = build_restaurant_tree()

traverse(restaurant_root)
