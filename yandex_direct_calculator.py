import webbrowser
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class YandexDirectCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Калькулятор автостратегий и ценностей Яндекс Директ")
        self.geometry("640x780")
        self.resizable(False, False)

        # Заголовок
        self.header = ctk.CTkLabel(
            self, 
            text="Яндекс Директ: Цены, Ценности и Бюджеты", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.header.pack(pady=(12, 5))

        # Создание вкладок
        self.tabview = ctk.CTkTabview(self, width=600, height=630)
        self.tabview.pack(padx=20, pady=5)

        self.tabview.add("Цена и Бюджет (CPA / W-Budget)")
        self.tabview.add("Ценность целей (Micro-goals)")
        self.tabview.add("Корректировки ставок (%)")

        self.setup_cpa_budget_tab()
        self.setup_value_tab()
        self.setup_adjustments_tab()

        # --- Подвал (Footer) ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(side="bottom", fill="x", pady=10)

        self.dev_label = ctk.CTkLabel(
            self.footer_frame, 
            text="Разработал Тимур: ", 
            font=ctk.CTkFont(size=12)
        )
        self.dev_label.pack(side="left", padx=(190, 0))

        self.tg_link = ctk.CTkLabel(
            self.footer_frame, 
            text="https://t.me/timurqobilov", 
            font=ctk.CTkFont(size=12, weight="bold", underline=True),
            text_color="#3B82F6",
            cursor="hand2"
        )
        self.tg_link.pack(side="left")
        self.tg_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://t.me/timurqobilov"))

    def create_input(self, parent, label_text, row, default_val="0"):
        lbl = ctk.CTkLabel(parent, text=label_text, anchor="w", font=ctk.CTkFont(size=12))
        lbl.grid(row=row, column=0, padx=12, pady=5, sticky="w")
        
        entry = ctk.CTkEntry(parent, width=170, placeholder_text=default_val)
        entry.grid(row=row, column=1, padx=12, pady=5)
        return entry

    def create_result(self, parent, label_text, row):
        lbl = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
        lbl.grid(row=row, column=0, padx=12, pady=5, sticky="w")
        
        val_lbl = ctk.CTkLabel(parent, text="—", font=ctk.CTkFont(size=12, weight="bold"), text_color="#1F6AA5", anchor="e")
        val_lbl.grid(row=row, column=1, padx=12, pady=5, sticky="e")
        return val_lbl

    # -------------------------------------------------------------------------
    # Вкладка 1: Расчет допустимой цены конверсии (CPA) и Недельного бюджета
    # -------------------------------------------------------------------------
    def setup_cpa_budget_tab(self):
        tab = self.tabview.tab("Цена и Бюджет (CPA / W-Budget)")

        self.avg_check = self.create_input(tab, "Средний чек (руб):", 0, "10000")
        self.margin_pct = self.create_input(tab, "Маржинальность (%):", 1, "30")
        self.drr_pct = self.create_input(tab, "Целевой ДРР от маржи (%):", 2, "40")
        self.cr_lead_to_pay = self.create_input(tab, "Конверсия лида в оплату (%):", 3, "20")
        self.target_conversions_week = self.create_input(tab, "Желаемо конверсий в неделю:", 4, "15")

        btn = ctk.CTkButton(tab, text="Рассчитать стратегии", command=self.calc_cpa_budget)
        btn.grid(row=5, column=0, columnspan=2, pady=12)

        self.res_max_cpa = self.create_result(tab, "Макс. допустимый CPO (продажа):", 6)
        self.res_target_cpl = self.create_result(tab, "Целевой CPL / CPA (заявка):", 7)
        self.res_min_budget = self.create_result(tab, "Мин. недельный бюджет (на 10 CPA):", 8)
        self.res_rec_budget = self.create_result(tab, "Реком. недельный бюджет (на цель):", 9)

    def calc_cpa_budget(self):
        try:
            check = float(self.avg_check.get() or 0)
            margin = float(self.margin_pct.get() or 0) / 100.0
            drr = float(self.drr_pct.get() or 0) / 100.0
            cr_pay = float(self.cr_lead_to_pay.get() or 0) / 100.0
            target_conv = float(self.target_conversions_week.get() or 0)

            # 1. Прибыль с 1 заказа
            profit_per_order = check * margin
            # 2. Максимальный CPO (Cost per Order) с учетом ДРР
            max_cpo = profit_per_order * drr
            # 3. Максимальный CPA / CPL для промежуточной цели (заявки)
            target_cpl = max_cpo * cr_pay

            # 4. Недельный бюджет для алгоритмов Яндекса:
            # Для обученности алгоритму желательно МИНИМУМ 10 конверсий в неделю на стратегию
            min_weekly_budget = target_cpl * 10
            # Выбранное пользователем желаемое число конверсий
            rec_weekly_budget = target_cpl * max(target_conv, 10)

            self.res_max_cpa.configure(text=f"{max_cpo:.2f} руб.")
            self.res_target_cpl.configure(text=f"{target_cpl:.2f} руб.")
            self.res_min_budget.configure(text=f"{min_weekly_budget:.2f} руб.")
            self.res_rec_budget.configure(text=f"{rec_weekly_budget:.2f} руб.")
        except ValueError:
            pass

    # -------------------------------------------------------------------------
    # Вкладка 2: Расчет Ценности Целевых Действий (Для составных микроцелей)
    # -------------------------------------------------------------------------
    def setup_value_tab(self):
        tab = self.tabview.tab("Ценность целей (Micro-goals)")

        self.main_sale_value = self.create_input(tab, "Ценность 1 Продажи (руб):", 0, "5000")
        self.cr_cart_to_sale = self.create_input(tab, "Корзина -> Продажа (%):", 1, "25")
        self.cr_form_to_sale = self.create_input(tab, "Заявка -> Продажа (%):", 2, "10")
        self.cr_call_to_sale = self.create_input(tab, "Звонок -> Продажа (%):", 3, "20")

        btn = ctk.CTkButton(tab, text="Рассчитать ценности микроцелей", command=self.calc_values)
        btn.grid(row=4, column=0, columnspan=2, pady=12)

        self.val_cart = self.create_result(tab, "Ценность цели 'Добавление в корзину':", 5)
        self.val_form = self.create_result(tab, "Ценность цели 'Отправка формы':", 6)
        self.val_call = self.create_result(tab, "Ценность цели 'Звонок в компанию':", 7)

    def calc_values(self):
        try:
            sale_val = float(self.main_sale_value.get() or 0)
            cr_cart = float(self.cr_cart_to_sale.get() or 0) / 100.0
            cr_form = float(self.cr_form_to_sale.get() or 0) / 100.0
            cr_call = float(self.cr_call_to_sale.get() or 0) / 100.0

            # Формула ценности микроцели = Ценность финальной продажи * CR перехода с микроцели в продажу
            value_cart = sale_val * cr_cart
            value_form = sale_val * cr_form
            value_call = sale_val * cr_call

            self.val_cart.configure(text=f"{value_cart:.2f} руб.")
            self.val_form.configure(text=f"{value_form:.2f} руб.")
            self.val_call.configure(text=f"{value_call:.2f} руб.")
        except ValueError:
            pass

    # -------------------------------------------------------------------------
    # Вкладка 3: Калькулятор Корректировки Ставок (%)
    # -------------------------------------------------------------------------
    def setup_adjustments_tab(self):
        tab = self.tabview.tab("Корректировки ставок (%)")

        self.base_cpa = self.create_input(tab, "Базовый CPA по кампании (руб):", 0, "500")
        self.segment_cpa = self.create_input(tab, "CPA выбранного сегмента (руб):", 1, "750")
        self.base_cr = self.create_input(tab, "Базовый CR кампании (%):", 2, "3.0")
        self.segment_cr = self.create_input(tab, "CR выбранного сегмента (%):", 3, "1.5")

        btn = ctk.CTkButton(tab, text="Рассчитать процент корректировки", command=self.calc_adjustments)
        btn.grid(row=4, column=0, columnspan=2, pady=12)

        self.res_adj_by_cpa = self.create_result(tab, "Корректировка по CPA:", 6)
        self.res_adj_by_cr = self.create_result(tab, "Корректировка по CR:", 7)

    def calc_adjustments(self):
        try:
            b_cpa = float(self.base_cpa.get() or 0)
            s_cpa = float(self.segment_cpa.get() or 0)
            b_cr = float(self.base_cr.get() or 0)
            s_cr = float(self.segment_cr.get() or 0)

            # Корректировка по CPA = ((Базовый CPA / CPA сегмента) - 1) * 100
            adj_cpa = ((b_cpa / s_cpa) - 1) * 100 if s_cpa > 0 else 0

            # Корректировка по CR = ((CR сегмента / Базовый CR) - 1) * 100
            adj_cr = ((s_cr / b_cr) - 1) * 100 if b_cr > 0 else 0

            # Форматирование текста вывода
            str_cpa = f"+{adj_cpa:.1f}%" if adj_cpa > 0 else f"{adj_cpa:.1f}%"
            str_cr = f"+{adj_cr:.1f}%" if adj_cr > 0 else f"{adj_cr:.1f}%"

            color_cpa = "#2FA572" if adj_cpa >= 0 else "#D55252"
            color_cr = "#2FA572" if adj_cr >= 0 else "#D55252"

            self.res_adj_by_cpa.configure(text=str_cpa, text_color=color_cpa)
            self.res_adj_by_cr.configure(text=str_cr, text_color=color_cr)
        except ValueError:
            pass


if __name__ == "__main__":
    app = YandexDirectCalculator()
    app.mainloop()