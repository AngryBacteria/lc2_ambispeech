from app.model.transcripts import (
    transcript_herzinfarkt,
    transcript_appendizitis,
    transcript_autounfall_1_0,
    transcript_bauchschmerzen_1_0,
    transcript_distorsion_1_0,
    transcript_dyspnoe_1_0,
    transcript_kopfschmerzen_1_0,
    transcript_stroke_1_0,
    transcript_autounfall_1_1,
    transcript_bauchschmerzen_1_1,
    transcript_distorsion_1_1,
    transcript_dyspnoe_1_1,
    transcript_kopfschmerzen_1_1,
    transcript_stroke_1_1,
)

medical_texts = {
    "with_noise_folder": "with_ambient_noise",
    "without_noise_folder": "without_ambient_noise",
    "files": [
        {
            "folder": "without_ambient_noise",
            "name": "APPENDIZITIS_1_0.wav",
            "transcript": transcript_appendizitis,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "APPENDIZITIS_BgndNoise.wav",
            "transcript": transcript_appendizitis,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "AUTOUNFALL_1_0_sprecher_A2FB2C8D.wav",
            "transcript": transcript_autounfall_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "AUTOUNFALL_1_0_sprecher_A2FB2C8D_BgndNoise.wav",
            "transcript": transcript_autounfall_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "AUTOUNFALL_1_1_sprecher_B5932A57.wav",
            "transcript": transcript_autounfall_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "AUTOUNFALL_1_1_sprecher_B5932A57_BgndNoise.wav",
            "transcript": transcript_autounfall_1_1,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "BAUCHSCHMERZEN_1_0_sprecher_7AF94A97.wav",
            "transcript": transcript_bauchschmerzen_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "BAUCHSCHMERZEN_1_0_sprecher_7AF94A97_BgndNoise.wav",
            "transcript": transcript_bauchschmerzen_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "BAUCHSCHMERZEN_1_1_sprecher_B8BDF020.wav",
            "transcript": transcript_bauchschmerzen_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "BAUCHSCHMERZEN_1_1_sprecher_B8BDF020_BgndNoise.wav",
            "transcript": transcript_bauchschmerzen_1_1,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "DISTORSION_1_0_sprecher_ADB71289.wav",
            "transcript": transcript_distorsion_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "DISTORSION_1_0_sprecher_ADB71289_BgndNoise.wav",
            "transcript": transcript_distorsion_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "DISTORSION_1_1_sprecher_0120B1C6.wav",
            "transcript": transcript_distorsion_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "DISTORSION_1_1_sprecher_0120B1C6_BgndNoise.wav",
            "transcript": transcript_distorsion_1_1,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "DYSPNOE_1_0_sprecher_8BD92A74.wav",
            "transcript": transcript_dyspnoe_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "DYSPNOE_1_0_sprecher_8BD92A74_BgndNoise.wav",
            "transcript": transcript_dyspnoe_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "DYSPNOE_1_1_sprecher_5F9E2F00.wav",
            "transcript": transcript_dyspnoe_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "DYSPNOE_1_1_sprecher_5F9E2F00_BgndNoise.wav",
            "transcript": transcript_dyspnoe_1_1,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "HERZINFARKT_1_0.wav",
            "transcript": transcript_herzinfarkt,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "HERZINFARKT_1_0_BgndNoise.wav",
            "transcript": transcript_herzinfarkt,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "KOPFSCHMERZEN_1_0_sprecher_EFA1AAD1.wav",
            "transcript": transcript_kopfschmerzen_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "KOPFSCHMERZEN_1_0_sprecher_EFA1AAD1_BgndNoise.wav",
            "transcript": transcript_kopfschmerzen_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "KOPFSCHMERZEN_1_1_sprecher_609B54E2.wav",
            "transcript": transcript_kopfschmerzen_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "KOPFSCHMERZEN_1_1_sprecher_609B54E2_BgndNoise.wav",
            "transcript": transcript_kopfschmerzen_1_1,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "STROKE_1_0_sprecher_4363D135.wav",
            "transcript": transcript_stroke_1_0,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "STROKE_1_0_sprecher_4363D135_BgndNoise.wav",
            "transcript": transcript_stroke_1_0,
            "synthetic": True,
            "noise": True,
        },
        {
            "folder": "without_ambient_noise",
            "name": "STROKE_1_1_sprecher_57576ED9.wav",
            "transcript": transcript_stroke_1_1,
            "synthetic": True,
            "noise": False,
        },
        {
            "folder": "with_ambient_noise",
            "name": "STROKE_1_1_sprecher_57576ED9_BgndNoise.wav",
            "transcript": transcript_stroke_1_1,
            "synthetic": True,
            "noise": True,
        },
    ],
}
