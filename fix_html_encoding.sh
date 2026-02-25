#!/bin/bash
#
# HTML Encoding Düzeltme Script
# HTML Encoding Fix Script
#
# Kullanım / Usage: ./fix_html_encoding.sh [dosya_adi]
# Örnek / Example: ./fix_html_encoding.sh V7_5_07226.txt
#

FILE="${1:-V7_5_07226.txt}"

echo "=========================================="
echo "HTML Encoding Düzeltme / HTML Encoding Fix"
echo "=========================================="
echo "Dosya / File: $FILE"
echo ""

if [ ! -f "$FILE" ]; then
    echo "❌ HATA: Dosya bulunamadı / ERROR: File not found"
    exit 1
fi

# Check for HTML entities
echo "Kontrol ediliyor / Checking for HTML entities..."
HTML_COUNT=$(grep -o "=&gt;" "$FILE" | wc -l)
echo "  =&gt; bulundu / found: $HTML_COUNT"

if [ "$HTML_COUNT" -eq 0 ]; then
    echo ""
    echo "✅ Dosya zaten doğru / File is already correct"
    echo "   Hiçbir HTML encoding yok / No HTML encoding found"
    exit 0
fi

# Backup original
BACKUP="${FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$FILE" "$BACKUP"
echo ""
echo "📦 Yedek oluşturuldu / Backup created:"
echo "   $BACKUP"

# Fix HTML entities
echo ""
echo "🔧 Düzeltiliyor / Fixing..."
sed -i 's/=&gt;/=>/g' "$FILE"
sed -i 's/&lt;/</g' "$FILE"
sed -i 's/&gt;/>/g' "$FILE"
sed -i 's/&amp;/\&/g' "$FILE"
sed -i 's/&quot;/"/g' "$FILE"

# Verify
NEW_COUNT=$(grep -o "=&gt;" "$FILE" | wc -l)
echo ""
if [ "$NEW_COUNT" -eq 0 ]; then
    echo "✅ Başarılı / Success!"
    echo "   $HTML_COUNT HTML entity düzeltildi / HTML entities fixed"
    echo "   Dosya Pine Script için hazır / File ready for Pine Script"
else
    echo "⚠️  Uyarı / Warning: Bazı sorunlar devam ediyor"
    echo "   $NEW_COUNT HTML entity hala var / HTML entities still remain"
fi

echo ""
echo "=========================================="
echo "Bitti / Done"
echo "=========================================="
