import flet as ft
from google import genai
client = genai.Client(api_key="AIzaSyCtlxRd42UAgNCfAi8P7dY-BCKY6dXwinw")

def main(page: ft.Page):
    page.title = "متخرج احكام التجويد الذكي "
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True
    
    page.scroll = ft.ScrollMode.AUTO

    title = ft.Container(
        content=ft.Text("مساعد التجويد  الحقيقي ", size=40, weight=ft.FontWeight.BOLD, color="white"),
        margin=ft.Margin(left=0, top=40, right=0, bottom=20)
    )

    verse_input = ft.TextField(
        label="أدخل الآية الكريمة بالتشكيل ",  
        width=500, 
        text_align=ft.TextAlign.CENTER,
        multiline=True
    )
    
    result_text = ft.Text(size=16, color="white", selectable=True)
    
    result_container = ft.Container(
        content=result_text,
        margin=10,
        padding=15,
        bgcolor="surfacevariant", 
        border_radius=10,
        width=500,
        visible=False
    )

    def analyze_tajweed(e):
        if not verse_input.value.strip():
            result_text.value = "الرجاء إدخال آية أولاً!"
            result_text.color = "red"
            result_container.visible = True
            page.update()
            return

        result_text.value = "جاري إرسال الآية إلى خوادم Google واستخراج الأحكام بدقة... ⏳"
        result_text.color = "amber"
        result_container.visible = True
        page.update()

        user_verse = verse_input.value
        
        try:
            prompt = (
                f"أنت خبير محترف في علم التجويد والقراءات. "
                f"قم باستخراج كافة أحكام التجويد الموجودة في هذه الآية الكريمة ملخصة فقط"
                f"(مثل الإظهار، الإدغام، الإخفاء، الإقلاب، القلقلة، والمدود)، مع تحديد موضع الحكم والسبب: "
                f"\"{user_verse}\""
            )

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            result_text.value = f"📖 الآية المدخلة: {user_verse}\n\n✨ نتائج التحليل الفوري:\n\n{response.text}"
            result_text.color = "green_accent"
            
        except Exception as error:
            result_text.value = f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {str(error)}"
            result_text.color = "red"
            
        page.update()

    analyze_button = ft.ElevatedButton(
        "استخراج أحكام التجويد الذكي", 
        on_click=analyze_tajweed, 
        bgcolor="green", 
        color="black"
    )

    page.add(title, verse_input, analyze_button, result_container)

ft.run(main)