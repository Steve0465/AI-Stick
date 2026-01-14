#!/bin/bash
echo "📊 AI STICK DOWNLOAD STATUS"
echo "============================"
echo ""
df -h /Volumes/AI_STICK | tail -1 | awk '{print "💾 Disk: " $3 " used / " $4 " free"}'
echo ""
echo "📥 Active downloads:"
ps aux | grep "wget.*zim" | grep -v grep | wc -l | xargs echo "   Running:"
echo ""
echo "📦 Downloaded files:"
find /Volumes/AI_STICK/knowledge -name "*.zim" -exec ls -lh {} \; 2>/dev/null | awk '{print "   " $9 ": " $5}'
echo ""
echo "📁 Folder sizes:"
du -sh /Volumes/AI_STICK/knowledge/*/ 2>/dev/null
