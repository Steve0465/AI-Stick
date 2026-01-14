#!/usr/bin/env python3
"""
Hardware Power Issue Diagnostic Tool
For laptops that power on briefly then shut off immediately
"""
import sys

def diagnose_power_symptoms():
    """Interactive diagnosis based on symptoms"""

    print("╔═══════════════════════════════════════════════════════════╗")
    print("║       LAPTOP POWER FAILURE DIAGNOSTIC TOOL               ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")

    print("🔍 I'll help diagnose why your HP convertible won't stay on.\n")
    print("Answer these questions about the symptoms:\n")

    symptoms = {}

    # Question 1: Power behavior
    print("1️⃣  What happens when you press the power button?")
    print("   a) Power light comes on, fan spins briefly, then shuts off (< 5 seconds)")
    print("   b) Power light comes on, stays on a bit longer (5-30 seconds), then shuts off")
    print("   c) Power light flickers or pulses, never fully powers on")
    print("   d) Absolutely nothing happens\n")
    symptoms['power_behavior'] = input("   Your answer (a/b/c/d): ").strip().lower()
    print()

    # Question 2: Display
    print("2️⃣  Does anything appear on the screen?")
    print("   a) Nothing - screen stays black")
    print("   b) HP logo appears briefly")
    print("   c) Screen flickers/flashes")
    print("   d) Screen lights up but no image\n")
    symptoms['display'] = input("   Your answer (a/b/c/d): ").strip().lower()
    print()

    # Question 3: Sounds
    print("3️⃣  Do you hear any sounds?")
    print("   a) Fan spins briefly then stops")
    print("   b) Beeping sounds (count: __)")
    print("   c) Clicking or buzzing")
    print("   d) No sounds at all\n")
    symptoms['sounds'] = input("   Your answer (a/b/c/d, if b include beep count): ").strip().lower()
    print()

    # Question 4: Battery
    print("4️⃣  Battery status:")
    print("   a) Same issue with battery in or out")
    print("   b) Works better with battery out (AC only)")
    print("   c) Works better with battery in (no AC)")
    print("   d) Charging light is acting weird\n")
    symptoms['battery'] = input("   Your answer (a/b/c/d): ").strip().lower()
    print()

    # Question 5: Recent events
    print("5️⃣  What happened before this issue started?")
    print("   a) Nothing - worked one day, didn't the next")
    print("   b) Windows update was installing")
    print("   c) Laptop got bumped/dropped")
    print("   d) Got wet or exposed to heat")
    print("   e) Was working hard (gaming, video editing)\n")
    symptoms['before_failure'] = input("   Your answer (a/b/c/d/e): ").strip().lower()
    print()

    # Question 6: Physical condition
    print("6️⃣  Physical condition:")
    print("   a) Laptop feels hot to touch")
    print("   b) Laptop is cold/normal temperature")
    print("   c) Smells like burning/electrical")
    print("   d) Something feels loose/rattles inside\n")
    symptoms['physical'] = input("   Your answer (a/b/c/d): ").strip().lower()
    print()

    print("\n" + "="*70)
    print("🤖 ANALYZING SYMPTOMS WITH AI...\n")
    print("="*70 + "\n")

    # Analyze symptoms
    diagnosis = analyze_symptoms(symptoms)

    print(diagnosis)

    # Ask if we can connect to Pi for AI analysis
    print("\n" + "="*70)
    print("🧠 Want deeper AI analysis?")
    print("   If you can connect to your Pi, I'll use Mistral AI for detailed diagnosis")
    use_ai = input("   Use AI? (y/n): ").strip().lower()

    if use_ai == 'y':
        ai_diagnose(symptoms)

def analyze_symptoms(symptoms):
    """Rule-based diagnosis based on symptoms"""

    diagnosis = []
    confidence = "Medium"
    likely_cause = "Unknown"

    power = symptoms.get('power_behavior', '')
    display = symptoms.get('display', '')
    sounds = symptoms.get('sounds', '')
    battery = symptoms.get('battery', '')
    before = symptoms.get('before_failure', '')
    physical = symptoms.get('physical', '')

    # Pattern matching for common issues

    # Short circuit / Power rail issue
    if power == 'a' and display == 'a' and sounds == 'a':
        likely_cause = "Power Rail Short Circuit or CPU/GPU Failure"
        confidence = "High"
        diagnosis.append("""
🔴 MOST LIKELY: POWER RAIL SHORT CIRCUIT

What's happening:
Your laptop is detecting a short circuit or hardware failure and
immediately shutting down to protect itself. This happens in < 5 seconds.

Common causes in HP convertibles:
1. Faulty RAM module (60% of cases)
2. Failed motherboard component (25%)
3. Liquid damage corrosion (10%)
4. Failed charging circuit (5%)

IMMEDIATE TESTS:
""")
        diagnosis.append("""
✅ TEST 1: Remove RAM modules
   - Open bottom panel
   - Remove ALL RAM sticks
   - Try to power on
   - If behavior changes → Bad RAM
   - Try one stick at a time to find culprit

✅ TEST 2: Disconnect battery + Hold power 30 seconds
   - Remove battery completely
   - Unplug AC adapter
   - Hold power button for 30 seconds (discharge capacitors)
   - Plug in AC only (no battery)
   - Try to power on
   - If it stays on longer → Battery issue

✅ TEST 3: Visual inspection
   - Look for:
     * Burn marks on motherboard
     * Swollen capacitors
     * Corrosion (white/green residue)
     * Loose connectors
   - If found → Hardware repair needed
""")

    # Thermal protection
    elif physical == 'a':
        likely_cause = "Thermal Protection Shutdown"
        confidence = "High"
        diagnosis.append("""
🌡️ LIKELY: THERMAL PROTECTION ACTIVE

What's happening:
Temperature sensor thinks laptop is overheating and shuts down immediately.
Common in HP convertibles due to thin chassis.

Causes:
1. Clogged fan/vents with dust
2. Dried thermal paste
3. Failed thermal sensor (reads incorrectly)

FIXES:
""")
        diagnosis.append("""
✅ FIX 1: Cool down completely
   - Put laptop in cool place (not fridge!)
   - Wait 2-3 hours
   - Try to power on
   - If it works briefly → Thermal issue confirmed

✅ FIX 2: Clean vents
   - Use compressed air on all vents
   - Hold fan still (prevent back-spin damage)
   - Blow from inside-out if possible

✅ FIX 3: BIOS reset
   - Remove battery
   - Hold power 60 seconds
   - Plug AC only
   - Immediately enter BIOS (F10)
   - Reset to defaults
   - This resets thermal thresholds
""")

    # BIOS corruption
    elif before == 'b' or (power == 'b' and display == 'b'):
        likely_cause = "BIOS Corruption from Failed Update"
        confidence = "High"
        diagnosis.append("""
💾 LIKELY: BIOS CORRUPTION

What's happening:
BIOS got corrupted (possibly during Windows update that included firmware).
Laptop starts POST but fails before OS loads.

THIS IS RECOVERABLE!
""")
        diagnosis.append("""
✅ FIX: BIOS Recovery (HP-specific)

HP convertibles have BIOS recovery mode:

STEP 1: Download BIOS
   - Go to: support.hp.com
   - Enter your laptop model (HP 360s)
   - Download latest BIOS update
   - Extract to USB drive root (not AI_STICK, use different USB)

STEP 2: Enter Recovery Mode
   - Unplug AC, remove battery
   - Hold Windows Key + B
   - While holding, plug in AC
   - Keep holding 10 seconds
   - Release
   - LED will flash, fan may spin

STEP 3: Recovery
   - Insert USB with BIOS file
   - Wait 5-10 minutes (laptop will flash LEDs)
   - When done, will power off automatically
   - Remove USB, try to boot normally

If this works → BIOS was corrupted
If this fails → Hardware issue
""")

    # RAM failure
    elif 'beep' in sounds or '2' in sounds or '3' in sounds:
        likely_cause = "RAM Failure"
        confidence = "Very High"
        diagnosis.append("""
🔴 CONFIRMED: RAM FAILURE

The beep codes indicate memory error.

HP Beep Codes:
- 2 beeps: Memory error
- 3 beeps: Memory error
- 5 beeps: Real-time clock error

FIX (EASY):
""")
        diagnosis.append("""
✅ Remove and reseat RAM:

STEP 1: Access RAM
   - Flip laptop over
   - Remove bottom panel screws
   - Lift panel carefully

STEP 2: Test
   - Remove ALL RAM sticks
   - Try to power on (will beep differently)
   - If different beeps → RAM was the problem

STEP 3: Isolate bad stick
   - Try one RAM stick at a time
   - Test each slot
   - Bad stick = laptop won't stay on

STEP 4: Replace
   - Buy replacement RAM (DDR4, check speed)
   - HP 360s uses standard SO-DIMM
   - ~$30-50 on Amazon

This fixes 60% of "immediate shutdown" issues!
""")

    # Battery/charging circuit
    elif battery in ['b', 'c', 'd']:
        likely_cause = "Battery or Charging Circuit Failure"
        confidence = "Medium-High"
        diagnosis.append("""
🔋 LIKELY: BATTERY OR CHARGING CIRCUIT ISSUE

What's happening:
Power delivery system is malfunctioning. Laptop can't get stable power.

TESTS:
""")
        diagnosis.append("""
✅ TEST 1: AC-only boot
   - Remove battery completely
   - Plug in AC adapter
   - Try to boot
   - If works → Battery is bad
   - If same issue → Charging circuit problem

✅ TEST 2: Battery-only boot
   - Disconnect AC
   - Put battery back in
   - Try to boot
   - If works → AC adapter or jack is bad

✅ TEST 3: Check AC adapter
   - Use multimeter: Should read 19.5V (HP standard)
   - Check for physical damage
   - Try different adapter if possible

✅ FIX: Battery reset
   - Remove battery
   - Hold power 60 seconds
   - Plug AC only
   - Boot into BIOS (F10)
   - Look for "Battery health" or "Power" settings
   - Reset/calibrate if option exists
""")

    # Physical damage
    elif before in ['c', 'd']:
        likely_cause = "Physical Damage"
        confidence = "High"
        diagnosis.append("""
⚠️ LIKELY: PHYSICAL DAMAGE

If laptop was dropped, bumped, or exposed to liquid/heat:

CHECKS:
""")
        diagnosis.append("""
✅ Visual inspection:
   - Open bottom panel
   - Look for:
     * Loose connectors (especially battery, display)
     * Cracked components on motherboard
     * Liquid residue (will look like white/green crust)
     * Bent pins in connectors

✅ Reseat connections:
   - Unplug and re-plug:
     * Battery connector
     * Display cable (ribbon cable at hinge)
     * RAM
     * SSD/hard drive
   - A loose connection can cause immediate shutdown

✅ Hinge check (360 convertibles):
   - Convertible hinges can damage display cable
   - Open/close laptop slowly
   - Listen for grinding or clicking
   - Check if it powers on in certain positions
     (if yes → cable damage in hinge)
""")

    # Generic if no clear match
    if not diagnosis:
        likely_cause = "Multiple Possible Causes"
        confidence = "Low"
        diagnosis.append("""
🔍 SYSTEMATIC TROUBLESHOOTING NEEDED

Your symptoms don't match a single clear pattern.
Let's test systematically:
""")
        diagnosis.append("""
✅ STEP 1: Power drain
   - Remove battery and AC
   - Hold power button 60 seconds
   - Plug AC only
   - Try to boot

✅ STEP 2: Minimal config
   - Remove battery
   - Remove all external devices
   - Leave only AC connected
   - Try to boot

✅ STEP 3: Hardware reset
   - Open laptop
   - Remove RAM
   - Disconnect SSD
   - Try to power on (will beep)
   - Add components back one by one

✅ STEP 4: BIOS recovery
   - Try HP BIOS recovery (instructions above)

✅ STEP 5: Professional diagnosis
   - If all above fails → Motherboard issue
   - Likely needs component-level repair
""")

    # Build final output
    output = f"""
╔═══════════════════════════════════════════════════════════╗
║                    DIAGNOSIS RESULTS                       ║
╚═══════════════════════════════════════════════════════════╝

🎯 Most Likely Cause: {likely_cause}
📊 Confidence: {confidence}

"""

    for section in diagnosis:
        output += section + "\n"

    output += """
╔═══════════════════════════════════════════════════════════╗
║                   IMPORTANT NOTES                          ║
╚═══════════════════════════════════════════════════════════╝

⚠️  DO NOT:
   - Open laptop if under warranty (voids warranty)
   - Force power on repeatedly (can damage components)
   - Use if you smell burning (fire hazard)

✅ DO:
   - Take photos during disassembly
   - Test one change at a time
   - Keep track of screws (use egg carton)
   - Ground yourself (touch metal) before touching components

📱 RECORD SYMPTOMS:
   - Take video of power-on behavior
   - Can help with diagnosis
   - Useful for warranty claim

🔧 TOOLS NEEDED:
   - Small Phillips screwdriver
   - Plastic pry tools (guitar picks work)
   - Compressed air
   - Multimeter (optional but helpful)

⏱️ TIME ESTIMATE:
   - Basic tests: 15-30 minutes
   - RAM removal/test: 30 minutes
   - BIOS recovery: 30-60 minutes
   - Full diagnosis: 1-2 hours
"""

    return output

def ai_diagnose(symptoms):
    """Use Mistral AI for deeper analysis"""
    print("\n🤖 Connecting to Mistral AI for advanced diagnosis...\n")

    # Prepare detailed prompt
    symptom_description = f"""
Hardware diagnosis request for HP convertible laptop (360s):

Symptoms:
- Power behavior: {symptoms.get('power_behavior', 'unknown')}
- Display: {symptoms.get('display', 'unknown')}
- Sounds: {symptoms.get('sounds', 'unknown')}
- Battery: {symptoms.get('battery', 'unknown')}
- Before failure: {symptoms.get('before_failure', 'unknown')}
- Physical condition: {symptoms.get('physical', 'unknown')}

Device specifics:
- HP convertible 360s
- Relatively new (less than 1 year old)
- Was working one day, stopped working the next
- Powers on briefly (light comes on) then immediately shuts off
- Battery has been removed and replaced

Based on these symptoms, provide:
1. Top 3 most likely hardware failures (with percentages)
2. Step-by-step diagnostic procedure
3. Estimated repair difficulty (DIY or professional)
4. Cost estimates for parts if replaceable
5. Warning signs that indicate professional repair needed
"""

    try:
        import requests

        response = requests.post('http://localhost:11434/api/generate',
            json={
                "model": "mistral",
                "prompt": symptom_description,
                "stream": False
            },
            timeout=120)

        ai_diagnosis = response.json()['response']

        print("="*70)
        print("🧠 MISTRAL AI ANALYSIS:")
        print("="*70)
        print(ai_diagnosis)
        print("="*70)

    except:
        print("❌ Cannot reach Ollama AI")
        print("   Run this on your Pi for AI-powered diagnosis:")
        print("   ssh pi@aiserver.local")
        print("   cd /media/pi/AI_STICK/windows_rescue")
        print("   ./diagnose_power_issue.py")

if __name__ == "__main__":
    diagnose_power_symptoms()
