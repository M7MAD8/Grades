#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    نظام تقدير درجات الطلاب - Student Grading System          ║
║                                   الإصدار 1.0                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

هذا البرنامج يقوم بتقييم أداء الطلاب بناءً على درجاتهم النهائية في الاختبار
ويوفر واجهة تفاعلية تسمح بإدخال درجات متعددة بشكل مستمر حتى يطلب المستخدم الخروج

المطور: نظام إدارة التعليم
التاريخ: 2024
"""

# =============================================================================
# استيراد المكتبات المطلوبة
# =============================================================================
import sys
import os
from datetime import datetime

# =============================================================================
# الثوابت والتعريفات العامة
# =============================================================================

# جدول التقديرات (الحدود الدنيا لكل تقدير)
GRADING_SCALE = {
    90: "ممتاز",
    75: "جيد جداً",
    60: "جيد",
    0: "ضعيف"
}

# رسائل التغذية الراجعة حسب التقدير
FEEDBACK_MESSAGES = {
    "ممتاز": "🎉 أداء متميز! أنت مثال يُحتذى به! استمر في التفوق!",
    "جيد جداً": "👍 أداء رائع! أنت على الطريق الصحيح نحو الامتياز!",
    "جيد": "📚 أداء جيد! مع القليل من الجهد الإضافي يمكنك تحقيق الأفضل!",
    "ضعيف": "💪 لا تيأس! تحتاج إلى بذل المزيد من الجهد. نؤمن بقدرتك على التحسن!"
}

# الإيموجيات لأنواع التقديرات
GRADE_EMOJIS = {
    "ممتاز": "🏆✨",
    "جيد جداً": "🌟⭐",
    "جيد": "📖✅",
    "ضعيف": "📝⚠️"
}

# =============================================================================
# الدوال المساعدة (Helper Functions)
# =============================================================================

def clear_screen():
    """
    مسح شاشة المحطة الطرفية
    تعمل على أنظمة Windows و Linux/Mac
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_grade_description(score: float) -> str:
    """
    تحويل الدرجة الرقمية إلى تقدير وصفي
    
    المعاملات:
        score (float): درجة الطالب (من 0 إلى 100)
    
    المخرجات:
        str: التقدير الوصفي (ضعيف، جيد، جيد جداً، ممتاز)
    
    مثال:
        >>> get_grade_description(95)
        'ممتاز'
        >>> get_grade_description(72)
        'جيد'
    """
    # ترتيب الحدود تنازلياً للتحقق من أعلى تقدير أولاً
    for min_score, grade in sorted(GRADING_SCALE.items(), reverse=True):
        if score >= min_score:
            return grade
    return "ضعيف"  # قيمة افتراضية (لن تصل هنا أبداً)


def get_grade_feedback(grade: str) -> str:
    """
    الحصول على رسالة تغذية راجعة مناسبة للتقدير
    
    المعاملات:
        grade (str): التقدير الوصفي
    
    المخرجات:
        str: رسالة تشجيعية مناسبة
    """
    return FEEDBACK_MESSAGES.get(grade, "استمر في التعلم والتطور!")


def get_grade_emoji(grade: str) -> str:
    """
    الحصول على إيموجي مناسب للتقدير
    
    المعاملات:
        grade (str): التقدير الوصفي
    
    المخرجات:
        str: إيموجي يعبر عن التقدير
    """
    return GRADE_EMOJIS.get(grade, "🎓")


def validate_score(score: float) -> bool:
    """
    التحقق من صحة الدرجة (وجودها في النطاق المسموح)
    
    المعاملات:
        score (float): الدرجة المراد التحقق منها
    
    المخرجات:
        bool: True إذا كانت الدرجة صحيحة، False إذا كانت خاطئة
    
    الشروط:
        - يجب أن تكون الدرجة رقماً
        - يجب أن تكون بين 0 و 100 شاملة
    """
    return 0 <= score <= 100


def is_exit_command(user_input: str) -> bool:
    """
    التحقق مما إذا كان المستخدم يريد الخروج من البرنامج
    
    المعاملات:
        user_input (str): النص المدخل من المستخدم
    
    المخرجات:
        bool: True إذا كان النص يعبر عن رغبة في الخروج
    
    ملاحظة: يتم التحقق من عدة كلمات مرادفة للخروج
    """
    exit_commands = ["خروج", "exit", "quit", "ق", "e", "q"]
    return user_input.strip().lower() in exit_commands


def parse_grade_input(user_input: str) -> tuple:
    """
    تحويل إدخال المستخدم إلى درجة رقمية صالحة
    
    المعاملات:
        user_input (str): النص المدخل من المستخدم
    
    المخرجات:
        tuple: (bool success, float score, str error_message)
               - success: True إذا كان التحويل ناجحاً
               - score: الدرجة المحولة (إذا نجحت)
               - error_message: رسالة الخطأ (إذا فشلت)
    
    مثال:
        >>> parse_grade_input("85")
        (True, 85.0, None)
        >>> parse_grade_input("abc")
        (False, 0, "خطأ: الرجاء إدخال رقم صحيح")
    """
    # إزالة المسافات الزائدة
    user_input = user_input.strip()
    
    # محاولة تحويل النص إلى رقم عشري
    try:
        score = float(user_input)
        
        # التحقق من صحة النطاق
        if not validate_score(score):
            return False, 0, f"❌ خطأ: الدرجة ({score}) يجب أن تكون بين 0 و 100"
        
        return True, score, None
        
    except ValueError:
        # فشل التحويل - النص ليس رقماً صالحاً
        return False, 0, "❌ خطأ: الرجاء إدخال رقم صحيح (مثال: 85, 73.5, 100)"


def display_welcome_message() -> None:
    """
    عرض رسالة الترحيب وتعليمات الاستخدام بشكل جميل ومنظم
    """
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + " " * 15 + "🎓 نظام تقدير درجات الطلاب 🎓" + " " * 15 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    print("\n📖 تعليمات الاستخدام:")
    print("   " + "─" * 50)
    print("   • أدخل درجة الطالب (رقم بين 0 و 100)")
    print("   • سيتم عرض التقدير المناسب مع ملاحظات تشجيعية")
    print("   • يمكنك إدخال درجات متعددة بشكل متتالي")
    print("   • اكتب كلمة 'خروج' أو 'exit' لإنهاء البرنامج")
    
    print("\n📊 جدول التقديرات:")
    print("   " + "─" * 50)
    print("   ┌──────────────┬─────────────────────┐")
    print("   │   نطاق الدرجة   │       التقدير        │")
    print("   ├──────────────┼─────────────────────┤")
    print("   │    90 - 100   │  🌟 ممتاز 🌟        │")
    print("   │    75 - 89    │  ⭐ جيد جداً ⭐      │")
    print("   │    60 - 74    │  📚 جيد 📚          │")
    print("   │     0 - 59    │  📝 ضعيف 📝         │")
    print("   └──────────────┴─────────────────────┘")
    
    print("\n💡 ملاحظة: يمكنك إدخال أرقام عشرية (مثال: 87.5)")
    print("=" * 70)


def display_result(score: float, grade: str, student_number: int) -> None:
    """
    عرض نتيجة التقييم للمستخدم بشكل منظم وجذاب
    
    المعاملات:
        score (float): درجة الطالب
        grade (str): التقدير الوصفي
        student_number (int): رقم الطالب في الجلسة الحالية
    """
    emoji = get_grade_emoji(grade)
    feedback = get_grade_feedback(grade)
    
    print("\n" + "═" * 70)
    print(f"📋 نتيجة الطالب #{student_number}")
    print("─" * 70)
    print(f"   {emoji}  الدرجة: {score:.2f} من 100")
    print(f"   🎯 التقدير: {grade}")
    print(f"   💬 التقييم: {feedback}")
    print("═" * 70)


def display_statistics(students_grades: list) -> None:
    """
    عرض إحصائيات الجلسة عند الخروج من البرنامج
    
    المعاملات:
        students_grades (list): قائمة بدرجات جميع الطلاب في الجلسة
    """
    if not students_grades:
        print("\n📊 لم يتم تقييم أي طالب في هذه الجلسة")
        return
    
    total_students = len(students_grades)
    average_score = sum(students_grades) / total_students
    max_score = max(students_grades)
    min_score = min(students_grades)
    
    # حساب عدد الطلاب في كل فئة تقدير
    grade_counts = {grade: 0 for grade in GRADING_SCALE.values()}
    for score in students_grades:
        grade = get_grade_description(score)
        grade_counts[grade] += 1
    
    print("\n" + "█" * 70)
    print("█" + " " * 20 + "📊 إحصائيات الجلسة 📊" + " " * 21 + "█")
    print("█" * 70)
    
    print(f"\n   👥 إجمالي الطلاب المقيمين: {total_students}")
    print(f"   📊 متوسط الدرجات: {average_score:.2f}")
    print(f"   🏆 أعلى درجة: {max_score:.2f}")
    print(f"   📉 أدنى درجة: {min_score:.2f}")
    
    print("\n   📈 توزيع التقديرات:")
    print("   " + "─" * 40)
    for grade, count in grade_counts.items():
        if count > 0:
            percentage = (count / total_students) * 100
            bar_length = int(percentage / 2)  # شريط بعرض 50 حرف كحد أقصى
            bar = "█" * bar_length + "░" * (50 - bar_length)
            print(f"   {grade:8} : {count:3} طالب ({percentage:5.1f}%) {bar}")
    
    print("\n" + "█" * 70)


def display_goodbye_message(students_count: int, start_time: datetime) -> None:
    """
    عرض رسالة الوداع عند إنهاء البرنامج
    
    المعاملات:
        students_count (int): عدد الطلاب الذين تم تقييمهم
        start_time (datetime): وقت بدء البرنامج
    """
    end_time = datetime.now()
    session_duration = end_time - start_time
    
    print("\n" + "=" * 70)
    print("👋 شكراً لاستخدام نظام تقدير درجات الطلاب!")
    print(f"📊 تم تقييم {students_count} طالب/طلاب في هذه الجلسة")
    print(f"⏱️  مدة الجلسة: {session_duration.seconds // 60} دقيقة و {session_duration.seconds % 60} ثانية")
    print("🌟 نتمنى للجميع التوفيق والنجاح!")
    print("=" * 70)


def handle_error(error_message: str, error_count: int) -> int:
    """
    معالجة الأخطاء وعرض رسائل مناسبة
    
    المعاملات:
        error_message (str): رسالة الخطأ
        error_count (int): عدد الأخطاء حتى الآن
    
    المخرجات:
        int: عدد الأخطاء المحدث
    """
    print(f"\n{error_message}")
    
    # نصائح إضافية حسب نوع الخطأ
    if "رقم" in error_message:
        print("💡 تلميح: استخدم أرقاماً فقط مع علامة عشرية اختيارية (مثال: 85 أو 73.5)")
    elif "بين 0 و 100" in error_message:
        print("💡 تلميح: الدرجات تكون عادة من 0 (أدنى) إلى 100 (أعلى)")
    
    error_count += 1
    if error_count >= 5:
        print("\n⚠️ ملاحظة: يبدو أنك تواجه صعوبة في الإدخال.")
        print("💡 تذكر: يمكنك كتابة 'خروج' في أي وقت لإنهاء البرنامج")
    
    return error_count


# =============================================================================
# الدالة الرئيسية (Main Function)
# =============================================================================

def main() -> None:
    """
    الدالة الرئيسية للبرنامج
    تتحكم في سير العمل وتتولى معالجة المدخلات وعرض المخرجات
    """
    # تسجيل وقت بدء البرنامج
    start_time = datetime.now()
    
    # عرض رسالة الترحيب
    display_welcome_message()
    
    # متغيرات الجلسة
    students_grades = []  # قائمة لتخزين درجات جميع الطلاب
    error_count = 0       # عداد الأخطاء المتتالية
    student_counter = 0   # عداد الطلاب المقيمين
    
    # الحلقة الرئيسية - تستمر حتى يطلب المستخدم الخروج
    while True:
        try:
            # طلب إدخال من المستخدم
            user_input = input("\n📝 أدخل درجة الطالب (أو 'خروج' للإنهاء): ").strip()
            
            # التحقق من أمر الخروج
            if is_exit_command(user_input):
                break
            
            # معالجة إدخال الدرجة
            success, score, error_msg = parse_grade_input(user_input)
            
            if not success:
                # تحديث عداد الأخطاء وعرض رسالة الخطأ
                error_count = handle_error(error_msg, error_count)
                continue  # العودة إلى بداية الحلقة
            
            # إعادة تعيين عداد الأخطاء عند الإدخال الصحيح
            error_count = 0
            
            # زيادة عداد الطلاب
            student_counter += 1
            
            # حساب التقدير
            grade = get_grade_description(score)
            
            # تخزين الدرجة للإحصائيات
            students_grades.append(score)
            
            # عرض النتيجة
            display_result(score, grade, student_counter)
            
        except KeyboardInterrupt:
            # معالجة حالة الضغط على Ctrl+C
            print("\n\n⚠️ تم مقاطعة البرنامج بواسطة المستخدم (Ctrl+C)")
            break
        
        except EOFError:
            # معالجة حالة نهاية الملف (End of File)
            print("\n\n⚠️ تم اكتشاف نهاية الإدخال")
            break
        
        except Exception as e:
            # معالجة أي أخطاء غير متوقعة
            print(f"\n⚠️ حدث خطأ غير متوقع: {type(e).__name__} - {e}")
            print("💡 الرجاء المحاولة مرة أخرى أو الاتصال بالدعم الفني")
            error_count = handle_error("حدث خطأ غير معروف", error_count)
    
    # عرض إحصائيات الجلسة
    display_statistics(students_grades)
    
    # عرض رسالة الوداع
    display_goodbye_message(student_counter, start_time)


# =============================================================================
# نقطة دخول البرنامج
# =============================================================================

if __name__ == "__main__":
    """
    يتم تنفيذ هذا الكود فقط عند تشغيل الملف مباشرة
    وليس عند استيراده كوحدة نمطية
    """
    main()
