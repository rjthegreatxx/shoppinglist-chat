import csv
import random

random.seed(42)

PRODUCTS = [
    # Wound Care
    ("Adhesive Bandages", "Sterile adhesive bandages for minor cuts and abrasions. Flexible fabric material conforms to body contours. Individually wrapped for hygiene. Available in standard sizes."),
    ("Sterile Gauze Pads", "Non-woven sterile gauze pads for wound dressing and absorption. Highly absorbent, lint-free material. Individually packaged. Available in 2x2, 4x4 inch sizes."),
    ("Medical Tape", "Hypoallergenic medical-grade tape for securing dressings and tubing. Breathable, moisture-resistant backing. Gentle on skin, removes without trauma. 1 inch x 10 yards per roll."),
    ("Elastic Bandage Roll", "Elastic compression bandage for sprains, strains, and swelling. Self-adherent, reusable design. Metal clip closure. Available in 2, 3, and 4 inch widths."),
    ("Wound Closure Strips", "Sterile adhesive wound closure strips for laceration closure. Microporous tape backing promotes healing. Hypoallergenic adhesive. Pack of 10 strips."),
    ("Hydrocolloid Dressings", "Occlusive hydrocolloid wound dressings for pressure ulcers and minor burns. Creates moist healing environment. Self-adhesive, waterproof outer layer. 4x4 inch size."),
    ("Transparent Film Dressings", "Sterile transparent polyurethane dressings for IV sites and superficial wounds. Waterproof, breathable membrane. Allows wound monitoring without removal. 6x8 cm."),
    ("Alginate Wound Dressing", "Highly absorbent calcium alginate dressing for heavily exuding wounds. Biodegradable natural fibers. Conforms to wound shape. Requires secondary dressing."),
    ("Silver Antimicrobial Dressing", "Silver-containing antimicrobial wound dressing for infected wounds. Broad-spectrum antimicrobial activity. Maintains moist wound environment. 4x4 inch sterile pad."),
    ("Foam Wound Dressing", "Soft silicone foam dressing for moderate to heavy exudate management. Non-adherent wound contact layer. Comfortable, conformable design. 10x10 cm size."),

    # Surgical Supplies
    ("Surgical Gloves", "Sterile latex surgical gloves for operative procedures. Powder-free, textured fingertips for superior grip. Anatomically shaped for reduced hand fatigue. Sizes 6.0 to 8.5."),
    ("Disposable Surgical Gown", "Sterile disposable surgical gown for operating room use. Fluid-resistant reinforced panels. Wraparound design with tie closure. AAMI Level 3 protection."),
    ("Surgical Drape Set", "Sterile disposable surgical drape set for procedure site isolation. Impervious barrier protection. Adhesive aperture for secure placement. Includes universal sheet and towels."),
    ("Suture Kit", "Sterile suture kit containing needle driver, tissue forceps, and scissors. Stainless steel instruments. Single-use disposable. Includes 3-0 nylon suture."),
    ("Scalpel Disposable", "Single-use sterile disposable scalpel with plastic handle. Carbon steel blade. Safety retractable blade design. Available in sizes 10, 11, 15, 22."),
    ("Surgical Stapler", "Disposable linear skin stapler for wound closure. Fires uniform staples for consistent results. Ergonomic grip for precise control. 35-staple capacity."),
    ("Electrosurgical Pencil", "Single-use electrosurgical pencil for cutting and coagulation. Holster for safe tip storage. Coiled cord design. Compatible with standard ESU generators."),
    ("Tissue Forceps", "Stainless steel tissue forceps for grasping and manipulating tissue. 1x2 teeth design. Autoclavable, reusable instrument. Available in 4.5 and 6 inch lengths."),
    ("Needle Driver", "Tungsten carbide-jawed needle driver for suture placement. Ratchet lock mechanism. Autoclavable stainless steel construction. 6 inch length."),
    ("Surgical Scissors", "Stainless steel surgical scissors for tissue dissection. Sharp-sharp tip configuration. Autoclavable, reusable design. Available in straight and curved styles."),

    # Diagnostic Equipment
    ("Digital Thermometer", "Fast-reading digital oral thermometer with 10-second readout. Fever alert with color-coded display. Flexible tip for comfort. Memory recall of last reading. Includes case."),
    ("Blood Pressure Cuff", "Aneroid sphygmomanometer for manual blood pressure measurement. Adult size cuff fits 9-13 inch arm circumference. D-ring cuff for single-handed use. Includes carrying case."),
    ("Pulse Oximeter", "Fingertip pulse oximeter for SpO2 and pulse rate monitoring. Large LED display. Auto power-off feature. Lanyard included. Suitable for adults."),
    ("Otoscope", "Diagnostic otoscope for ear canal examination. Halogen illumination system. Wide-angle speculum. Includes 4 disposable specula. Requires 2 AA batteries."),
    ("Stethoscope", "Dual-head stethoscope for cardiac and pulmonary auscultation. Stainless steel chestpiece. 27-inch tubing. Includes extra ear tips. Suitable for adult and pediatric use."),
    ("Glucometer", "Blood glucose monitoring system for diabetes management. 5-second test results. 500-reading memory with date and time. No coding required. Includes 10 test strips."),
    ("Ophthalmoscope", "Direct ophthalmoscope for fundus examination. Multiple apertures and filters. Rheostat-controlled illumination. Rechargeable handle compatible."),
    ("Reflex Hammer", "Taylor percussion hammer for neurological reflex testing. Triangular rubber head. Stainless steel handle. Dual-purpose design with brush and needle."),
    ("Tongue Depressors", "Sterile wooden tongue depressors for oral examination. Smooth, splinter-free finish. Individually wrapped. Box of 100. Suitable for pediatric and adult use."),
    ("Penlight", "Medical diagnostic penlight for pupil and oral examination. Bright LED illumination. Pupil gauge printed on barrel. Disposable, single-patient use."),

    # IV & Infusion
    ("IV Catheter", "Safety peripheral IV catheter with passive needle retraction. Polyurethane catheter. Blood control septum reduces exposure. Available in 18G, 20G, 22G, 24G."),
    ("IV Administration Set", "Sterile IV administration set with 60-inch tubing. 15-drop drip chamber. In-line slide clamp. Leur-lock connector. Latex-free construction."),
    ("Saline Flush Syringe", "Pre-filled 0.9% sodium chloride flush syringe. 10mL volume. Leur-lock tip. Ready-to-use, single-dose design. Sterile, preservative-free solution."),
    ("Extension Set", "IV extension set with T-port injection site. 7-inch length. Clamp included. Leur-lock connections. Latex-free, DEHP-free construction."),
    ("Needleless Connector", "Positive displacement needleless connector for IV access. Reduces catheter occlusion. Leur-lock design. Latex-free. Single-use, sterile."),
    ("Infusion Pump Tubing", "Dedicated infusion pump administration set with anti-free-flow mechanism. Compatible with major pump brands. Latex-free. 100-inch length."),
    ("Arm Board", "Disposable padded arm board for IV site immobilization. Adjustable hook-and-loop strap. Latex-free foam padding. Available in adult and pediatric sizes."),
    ("IV Dressing Kit", "Transparent IV site dressing kit with CHG-impregnated disc. Includes dressing, stat lock stabilization device, and label. Reduces CLABSI risk."),

    # Respiratory
    ("Oxygen Mask Adult", "Adult non-rebreather oxygen mask for high-flow oxygen delivery. Soft, clear PVC construction. 7-foot supply tubing included. One-way exhalation valves."),
    ("Nasal Cannula", "Disposable nasal cannula for low-flow oxygen delivery. Soft, comfortable prongs. 7-foot supply tubing. Adult size. Latex-free construction."),
    ("Nebulizer Kit", "Small volume nebulizer kit for aerosol medication delivery. Includes mouthpiece, T-piece, and 6-foot tubing. Works with standard air compressors. Single-patient use."),
    ("Suction Catheter", "Flexible suction catheter for oral and nasal suctioning. Rounded distal tip. Vacuum control vent. Available in 8Fr, 10Fr, 12Fr, 14Fr sizes."),
    ("Bag Valve Mask", "Manual resuscitator bag valve mask for emergency ventilation. 1600mL adult bag. Clear mask for visual monitoring. PEEP valve compatible. Includes oxygen reservoir."),
    ("Tracheostomy Care Kit", "Sterile tracheostomy care kit for stoma maintenance. Includes twill ties, cotton-tipped applicators, and hydrogen peroxide. Single-use."),
    ("Incentive Spirometer", "Volumetric incentive spirometer for deep breathing exercises. Visual feedback with movable indicator. 4000mL capacity. Includes mouthpiece and instructions."),

    # Patient Monitoring
    ("ECG Electrode", "Disposable ECG electrodes for cardiac monitoring. Ag/AgCl sensing element. Foam backing for patient comfort. Latex-free adhesive. Pack of 50."),
    ("SpO2 Sensor", "Reusable adult finger-clip SpO2 sensor. Compatible with major monitor brands. 3-foot cable. Wavelength 660/940nm. Suitable for adults over 40kg."),
    ("Blood Pressure Cuff Disposable", "Single-use disposable blood pressure cuff for infection control. Available in small, regular, large adult, and thigh sizes. Nylon bladder construction."),
    ("Temperature Probe Cover", "Disposable probe covers for electronic thermometers. Latex-free. Box of 100. Fits standard oral and rectal probes. Maintains measurement accuracy."),

    # Personal Protective Equipment
    ("Surgical Mask", "ASTM Level 3 surgical mask for fluid splash protection. Tri-layer filtration. Adjustable nose wire. Soft ear loops. Box of 50 masks."),
    ("N95 Respirator", "NIOSH-approved N95 filtering facepiece respirator. 95% filtration efficiency. Adjustable nose clip. Foam nose seal for comfort. Pack of 20."),
    ("Face Shield", "Full-face splash protection shield. Anti-fog coating. Adjustable headband. Lightweight, comfortable design. Reusable with proper disinfection."),
    ("Exam Gloves Nitrile", "Powder-free nitrile examination gloves. Textured fingertips for grip. Beaded cuff for donning. Latex-free, chemical resistant. Box of 100."),
    ("Isolation Gown", "Disposable isolation gown for contact and droplet precautions. AAMI Level 2 protection. Knit cuffs. Tie closure at neck and back. Pack of 10."),
    ("Shoe Covers", "Disposable non-skid shoe covers for clean room and isolation use. Fluid-resistant. Elastic opening for easy donning. Box of 100 pairs."),
    ("Bouffant Cap", "Disposable bouffant cap for hair containment. Lightweight polypropylene. One size fits most. Box of 100. Available in blue and white."),

    # Lab Supplies
    ("Blood Collection Tube", "Evacuated blood collection tube with EDTA anticoagulant. Lavender top. 4mL draw volume. For hematology testing. Safety needle required."),
    ("Urine Collection Cup", "Sterile specimen collection cup for urinalysis. Leak-proof lid. Graduated volume markings. 4oz capacity. Includes label for patient identification."),
    ("Lancet Safety", "Single-use safety lancet for capillary blood sampling. 28-gauge needle. Automatic retraction after use. Reduces needlestick injury risk. Box of 100."),
    ("Culturette Swab", "Rayon-tipped culturette swab for microbiological specimen collection. Transport medium included. Maintains organism viability. For aerobic and anaerobic cultures."),
    ("Centrifuge Tubes", "Polypropylene conical centrifuge tubes. 15mL and 50mL sizes available. Leak-proof screw cap. Graduated markings. Autoclavable. Pack of 50."),
    ("Microscope Slides", "Pre-cleaned microscope slides for histology and cytology. Frosted end for labeling. 25x75mm size. 1mm thickness. Box of 72."),
    ("Pipette Tips", "Universal fit pipette tips for multichannel and single-channel pipettors. Aerosol-resistant filter optional. Graduated volume markings. Rack of 96."),
    ("Petri Dish", "Sterile polystyrene Petri dishes for microbiological culture. 100x15mm size. Stackable design. Vented lid option available. Pack of 20."),

    # Mobility & Rehab
    ("Walker Standard", "Lightweight aluminum standard walker for ambulation assistance. Adjustable height from 32 to 37 inches. Non-skid rubber tips. 350 lb weight capacity."),
    ("Cane Quad", "Quad cane with four-point base for increased stability. Offset handle for natural grip. Adjustable height. Non-skid rubber tips. Supports up to 300 lbs."),
    ("Wheelchair Standard", "Standard folding wheelchair with swing-away footrests. 18-inch seat width. Desk-length armrests. Solid tires. 250 lb weight capacity."),
    ("Transfer Belt", "Padded transfer belt for safe patient transfers. Quick-release buckle. Adjustable size. Durable nylon webbing. Supports up to 400 lbs."),
    ("Compression Stockings", "Graduated compression stockings for DVT prevention and edema management. 15-20 mmHg compression. Knee-high length. Available in small to extra-large."),
    ("Foam Wedge Pillow", "Therapeutic foam wedge pillow for positioning and pressure relief. Firm, supportive foam. Removable, washable cover. 10x24x24 inch size."),
    ("Cold Pack Reusable", "Reusable cold pack for pain relief and swelling reduction. Flexible when frozen. Soft cloth cover included. 6x9 inch size. Refreezable."),
    ("Hot Pack Reusable", "Reusable moist heat pack for muscle relaxation. Hydrophilic beads retain heat. Machine washable cover. Microwave-safe. 6x12 inch size."),

    # Nutrition & Feeding
    ("Enteral Feeding Bag", "Sterile enteral feeding bag for tube feeding administration. 1000mL capacity. Attached 60-inch tubing. Anti-free-flow clamp. Includes Y-port for medication."),
    ("Feeding Tube", "Nasogastric feeding tube for enteral nutrition. Polyurethane construction. Radiopaque stripe for X-ray verification. Available in 8Fr, 10Fr, 12Fr, 16Fr."),
    ("Oral Syringe", "Oral medication syringe for enteral drug administration. 10mL and 60mL sizes. Color-coded tip incompatible with IV lines. Graduated markings. Latex-free."),
    ("Thickening Agent", "Starch-based beverage thickener for dysphagia management. Nectar and honey consistency levels. Unflavored, mixes with any beverage. 10oz canister."),

    # Urology
    ("Foley Catheter", "Silicone Foley catheter for urinary drainage. 30cc balloon. Available in 14Fr, 16Fr, 18Fr. Smooth tip for atraumatic insertion. Latex-free."),
    ("Urinary Drainage Bag", "Sterile urinary drainage bag for indwelling catheter. 2000mL capacity. Anti-reflux valve. Hanger and hook included. Drip chamber for output monitoring."),
    ("Catheter Insertion Kit", "Sterile Foley catheter insertion tray. Includes drapes, gloves, antiseptic solution, and syringe. Complete setup for indwelling catheterization."),
    ("External Catheter", "Male external urinary catheter for incontinence management. Self-adhesive design. Soft latex construction. 36-inch drainage tubing. Available in small, medium, large."),

    # Orthopedic
    ("Arm Sling", "Universal arm sling for shoulder and forearm immobilization. Adjustable neck strap. Padded for comfort. One size fits most adults. Machine washable."),
    ("Thumb Splint", "Rigid thumb spica splint for thumb injuries and CMC arthritis. Aluminum core. Foam padding. Adjustable hook-and-loop straps. Available left and right."),
    ("Ankle Brace", "Lace-up ankle brace for sprain support and prevention. Medial and lateral stays for stability. Fits standard footwear. Available in small through extra-large."),
    ("Cervical Collar", "Semi-rigid cervical collar for neck immobilization. Adjustable height. Padded chinpiece. Washable cover. Available in soft and firm styles."),
    ("Knee Immobilizer", "Foam knee immobilizer for post-operative or injury immobilization. Adjustable hook-and-loop straps. Universal fit. Available in 16, 20, and 24 inch lengths."),

    # Pharmacy & Medication
    ("Medication Cup", "Disposable graduated medication cups for oral medication dispensing. 1oz and 2oz sizes. Clearly printed graduations in mL, tsp, tbsp, and oz. Pack of 100."),
    ("Pill Crusher", "Pill crusher and splitter for medication administration. Stainless steel blades. Medication storage compartment. Easy-clean design. Includes storage cup."),
    ("Insulin Syringe", "Insulin syringe with permanently attached needle. 1mL capacity. 28G x 1/2 inch needle. Permanently bonded needle minimizes dead space. Box of 100."),
    ("Sharps Container", "Puncture-resistant sharps disposal container. 1-quart capacity. One-hand activation drop-in opening. Secure lid for transport. Biohazard label included."),
    ("Medication Organizer", "7-day medication organizer with AM/PM compartments. Large, easy-open lids. Clear compartments for visual inspection. Dishwasher-safe tray."),
]

categories = [
    "Wound Care", "Surgical Supplies", "Diagnostic Equipment",
    "IV & Infusion", "Respiratory", "Patient Monitoring",
    "PPE", "Lab Supplies", "Mobility & Rehab",
    "Nutrition & Feeding", "Urology", "Orthopedic", "Pharmacy"
]

def generate_id(index):
    prefix = random.choice(["MED", "SUP", "SRG", "DX", "LAB"])
    return f"{prefix}-{str(index).zfill(6)}"

output_path = "data/products.csv"

import os
os.makedirs("data", exist_ok=True)

rows = []
for i, (name, description) in enumerate(PRODUCTS):
    product_id = generate_id(i + 1)
    rows.append((product_id, name, description))

with open(output_path, "w", newline="") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

print(f"Generated {len(rows)} products → {output_path}")
