<div dir="rtl">

## مزایای استفاده از Cookie به جای Authorization Header

### محافظت در برابر XSS

با استفاده از ویژگی <code>HttpOnly</code>، کدهای JavaScript نمی‌توانند مستقیماً به <code>Cookie</code> دسترسی داشته باشند. بنابراین در صورت وجود حمله <code>XSS</code>، امکان سرقت مستقیم <code>Token</code> توسط JavaScript کاهش پیدا می‌کند.

### کاهش خطر CSRF

<code>Cookie</code>ها به صورت خودکار توسط مرورگر ارسال می‌شوند، بنابراین <code>Cookie</code> به تنهایی از حملات <code>CSRF</code> جلوگیری نمی‌کند. برای کاهش این خطر در پروژه از ویژگی زیر استفاده شده است:

<code>SameSite="Lax"</code>

این ویژگی باعث محدود شدن ارسال <code>Cookie</code> در برخی درخواست‌های <code>Cross-Site</code> می‌شود و خطر <code>CSRF</code> را کاهش می‌دهد. در برنامه‌های حساس‌تر می‌توان از <code>CSRF Token</code> نیز استفاده کرد.

همچنین با تنظیم <code>Secure=True</code>، <code>Cookie</code> فقط از طریق ارتباط <code>HTTPS</code> ارسال می‌شود و احتمال افشای <code>Token</code> در ارتباطات ناامن کاهش می‌یابد.

### مدیریت خطاهای Token

اگر <code>Token</code> منقضی یا نامعتبر باشد، سیستم درخواست را رد کرده و خطای <code>401 Unauthorized</code> برمی‌گرداند. همچنین <code>user_id</code> و نوع <code>Token</code> بررسی می‌شوند تا فقط <code>Token</code>های معتبر و مناسب برای هر عملیات پذیرفته شوند.

</div>