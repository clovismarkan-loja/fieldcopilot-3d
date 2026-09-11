# Gera os assets Blender da landing page Field Copilot (sequencias WebP p/ canvas-scrub)
# Uso: blender.exe -b --python render_assets.py -- <asset>
# Assets: hero360 conjunto360 camera_zoom bateria_giro lanterna fone_encaixe montagem relogio_giro final_perfil
import bpy
import math
import sys
import os
from mathutils import Vector

BASE = r"D:\loja\Teste 3d\Headset"
OUT = os.path.join(BASE, "site", "assets")
ASSET = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "hero360"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- mundo escuro + luz de estudio ----------
world = bpy.data.worlds.new("W")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.005, 0.005, 0.006, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0

def _aponta(obj, alvo=(0.0, 0.0, 0.0)):
    d = Vector(alvo) - obj.location
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = d.to_track_quat('-Z', 'Y')

def luz_estudio(escala=1.0):
    # strip softbox frontal: aparece como reflexo retangular nas lentes/vidros
    bpy.ops.object.light_add(type='AREA', location=(0.55 * escala, -0.15 * escala, 0.38 * escala))
    strip = bpy.context.active_object
    strip.data.shape = 'RECTANGLE'
    strip.data.size = 1.1 * escala
    strip.data.size_y = 0.10 * escala
    strip.data.energy = 1.5 * escala * escala
    _aponta(strip)
    bpy.ops.object.light_add(type='AREA', location=(0.35 * escala, -0.35 * escala, 0.45 * escala))
    key = bpy.context.active_object
    key.data.energy = 5 * escala * escala
    key.data.size = 0.5 * escala
    key.rotation_euler = (math.radians(42), math.radians(18), math.radians(38))
    bpy.ops.object.light_add(type='AREA', location=(-0.45 * escala, 0.25 * escala, 0.25 * escala))
    fill = bpy.context.active_object
    fill.data.energy = 1.6 * escala * escala
    fill.data.size = 0.7 * escala
    fill.rotation_euler = (math.radians(-55), math.radians(-35), math.radians(-20))
    bpy.ops.object.light_add(type='AREA', location=(0.0, 0.5 * escala, -0.1 * escala))
    rim = bpy.context.active_object
    rim.data.energy = 7 * escala * escala
    rim.data.size = 0.4 * escala
    rim.rotation_euler = (math.radians(255), 0, 0)

def cam_nova(lens=70):
    cd = bpy.data.cameras.new("cam")
    cd.clip_start = 0.001
    cd.lens = lens
    cam = bpy.data.objects.new("cam", cd)
    scene.collection.objects.link(cam)
    scene.camera = cam
    return cam

def mira(cam, loc, alvo):
    cam.location = loc
    d = Vector(alvo) - Vector(loc)
    cam.rotation_mode = 'QUATERNION'
    cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')

def setup_render(w=1600, h=900, qualidade=80):
    for eng in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE', 'CYCLES'):
        try:
            scene.render.engine = eng
            break
        except TypeError:
            continue
    scene.render.resolution_x = w
    scene.render.resolution_y = h
    scene.render.image_settings.file_format = 'WEBP'
    scene.render.image_settings.quality = qualidade
    scene.render.image_settings.color_mode = 'RGB'

def render_para(caminho):
    scene.render.filepath = caminho
    bpy.ops.render.render(write_still=True)

def melhora_materiais():
    """Lentes mais realistas (coat + lisas) e fita com material de tecido (trama + sheen)."""
    def _set(bsdf, nome, val):
        try:
            bsdf.inputs[nome].default_value = val
        except (KeyError, TypeError):
            pass
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        b = m.node_tree.nodes.get("Principled BSDF")
        if not b:
            continue
        n = m.name.lower()
        if n.startswith("vidro_lente"):
            _set(b, "Roughness", 0.02)
            _set(b, "IOR", 1.5)
            _set(b, "Coat Weight", 1.0)
            _set(b, "Coat Roughness", 0.02)
        elif n.startswith("lente_interna"):
            _set(b, "Roughness", 0.04)
            _set(b, "Base Color", (0.010, 0.014, 0.055, 1.0))  # coating azulado de optica
            _set(b, "Coat Weight", 0.8)
        elif n.startswith("elastico") and "TramaBump" not in [x.label for x in m.node_tree.nodes]:
            nt = m.node_tree
            _set(b, "Roughness", 0.93)
            _set(b, "Sheen Weight", 0.22)
            tc = nt.nodes.new("ShaderNodeTexCoord")
            w1 = nt.nodes.new("ShaderNodeTexWave")
            w1.wave_type = 'BANDS'
            w1.bands_direction = 'X'
            w1.inputs["Scale"].default_value = 1100.0
            w1.inputs["Distortion"].default_value = 6.0
            w2 = nt.nodes.new("ShaderNodeTexWave")
            w2.wave_type = 'BANDS'
            w2.bands_direction = 'Y'
            w2.inputs["Scale"].default_value = 1100.0
            w2.inputs["Distortion"].default_value = 6.0
            soma = nt.nodes.new("ShaderNodeMath")
            soma.operation = 'ADD'
            bump = nt.nodes.new("ShaderNodeBump")
            bump.label = "TramaBump"
            bump.inputs["Strength"].default_value = 0.12
            bump.inputs["Distance"].default_value = 0.0004
            nt.links.new(tc.outputs["Object"], w1.inputs["Vector"])
            nt.links.new(tc.outputs["Object"], w2.inputs["Vector"])
            nt.links.new(w1.outputs["Fac"], soma.inputs[0])
            nt.links.new(w2.outputs["Fac"], soma.inputs[1])
            nt.links.new(soma.outputs["Value"], bump.inputs["Height"])
            nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])

def importa(glb):
    antes = set(scene.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(BASE, glb))
    melhora_materiais()
    return [o for o in scene.objects if o not in antes]

def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)

def orbita_seq(nome, alvo, raio0, raio1, elev0, elev1, nf, lens=70, ang0=20.0, giro=360.0):
    cam = cam_nova(lens)
    pasta = os.path.join(OUT, nome)
    os.makedirs(pasta, exist_ok=True)
    for f in range(nf):
        t = f / (nf - 1)
        ang = math.radians(ang0 + giro * t)
        raio = raio0 + (raio1 - raio0) * smoothstep(t)
        elev = elev0 + (elev1 - elev0) * smoothstep(t)
        loc = (alvo[0] + raio * math.cos(ang) * math.cos(elev),
               alvo[1] + raio * math.sin(ang) * math.cos(elev),
               alvo[2] + raio * math.sin(elev))
        mira(cam, loc, alvo)
        render_para(os.path.join(pasta, f"f{f:03d}"))
    print(f"OK {nome}: {nf} frames")

# ================= assets =================
if ASSET == "hero360":
    importa("headset_montado_v3.glb")
    luz_estudio(1.0)
    setup_render()
    orbita_seq("seq_hero_360", (0.0, 0.0, 0.02), 0.60, 0.44, math.radians(12), math.radians(6), 120, lens=75)

elif ASSET == "hero_zoom":
    # hero novo: frontal, conjunto embaixo do quadro, zoom ate a lente da camera -> quase preto
    # trajetoria igual ao camera_zoom ("o olho"), transposta pela posicao do modulo no conjunto POS_DIR
    importa("headset_montado_v3.glb")
    luz_estudio(1.0)
    setup_render()
    cam = cam_nova(70)
    pasta = os.path.join(OUT, "seq_hero_zoom")
    os.makedirs(pasta, exist_ok=True)
    POS_DIR = Vector((0.036, -0.097, 0.025))
    # frontal (camera em +X); alvo acima do centro empurra o conjunto p/ baixo do quadro
    p0, a0, l0 = Vector((0.54, 0.0, 0.06)), Vector((0.0, 0.0, 0.048)), 70.0
    # ponto "o olho" transposto p/ o conjunto
    p1, a1 = Vector((0.085, -0.052, 0.012)) + POS_DIR, Vector((0.030, -0.004, 0.0)) + POS_DIR
    # aproximacao final: quase colado na lente -> quadro praticamente preto
    p2, a2, l2 = Vector((0.079, -0.104, 0.0255)), Vector((0.066, -0.101, 0.025)), 95.0
    NF = 120
    if "--" in sys.argv and "prova" in sys.argv:
        quadros = [0, 60, 96, 119]
    else:
        quadros = range(NF)
    for f in quadros:
        t = smoothstep(f / (NF - 1))
        if t < 0.8:
            s = t / 0.8
            loc = p0.lerp(p1, s)
            alvo = a0.lerp(a1, s)
        else:
            s = (t - 0.8) / 0.2
            loc = p1.lerp(p2, s)
            alvo = a1.lerp(a2, s)
        cam.data.lens = l0 + (l2 - l0) * t
        mira(cam, loc, alvo)
        render_para(os.path.join(pasta, f"f{f:03d}"))
    print(f"OK seq_hero_zoom: {len(list(quadros))} frames")

elif ASSET == "conjunto360":
    importa("headset_montado_v3.glb")
    luz_estudio(1.0)
    setup_render()
    orbita_seq("seq_conjunto_360", (0.0, 0.0, 0.015), 0.55, 0.55, math.radians(22), math.radians(10), 120, lens=70)

elif ASSET == "camera_zoom":
    importa("novo_modulo_camera_v3.glb")
    luz_estudio(0.6)
    setup_render()
    cam = cam_nova(70)
    pasta = os.path.join(OUT, "seq_camera_zoom")
    os.makedirs(pasta, exist_ok=True)
    p0, a0, l0 = Vector((0.21, -0.24, 0.13)), Vector((-0.02, 0.0, 0.0)), 70.0
    p1, a1, l1 = Vector((0.085, -0.052, 0.012)), Vector((0.030, -0.004, 0.0)), 95.0
    for f in range(90):
        t = smoothstep(f / 89.0)
        cam.data.lens = l0 + (l1 - l0) * t
        mira(cam, p0.lerp(p1, t), a0.lerp(a1, t))
        render_para(os.path.join(pasta, f"f{f:03d}"))
    print("OK seq_camera_zoom: 90 frames")

elif ASSET == "bateria_giro":
    importa("modulo_bateria_v3.glb")
    luz_estudio(0.6)
    setup_render()
    # termina exatamente no enquadramento dos stills da lanterna (continuidade do cross-fade)
    orbita_seq("seq_bateria_giro", (0.005, 0.0, 0.0), 0.30, 0.2404, math.radians(18), math.radians(16.9), 90, lens=70, ang0=-47.6, giro=360)

elif ASSET == "lanterna":
    objs = importa("modulo_bateria_v3.glb")
    luz_estudio(0.6)
    setup_render()
    # (glare do LED fica por conta de overlay CSS na pagina)
    mat_led = None
    for m in bpy.data.materials:
        if m.name.startswith("LED") and m.use_nodes:
            mat_led = m
    # mesma camera do frame final do seq_bateria_giro (alvo 0.005, raio 0.2404, elev 16.9, ang -47.6)
    cam = cam_nova(70)
    _r, _e, _a = 0.2404, math.radians(16.9), math.radians(-47.6)
    _loc = (0.005 + _r * math.cos(_a) * math.cos(_e), _r * math.sin(_a) * math.cos(_e), _r * math.sin(_e))
    mira(cam, _loc, (0.005, 0.0, 0.0))
    pasta = os.path.join(OUT, "stills")
    os.makedirs(pasta, exist_ok=True)
    if mat_led:
        b = mat_led.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Emission Strength"].default_value = 0.0
    render_para(os.path.join(pasta, "img_lanterna_off"))
    if mat_led:
        b = mat_led.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Emission Strength"].default_value = 60.0
    # feixe fake: spot saindo do LED
    bpy.ops.object.light_add(type='SPOT', location=(0.027, 0.0, 0.0))
    spot = bpy.context.active_object
    spot.data.energy = 8.0
    spot.data.spot_size = math.radians(55)
    spot.data.spot_blend = 0.6
    spot.rotation_euler = (0, math.radians(90), 0)
    render_para(os.path.join(pasta, "img_lanterna_on"))
    print("OK lanterna: 2 stills")

elif ASSET == "fone_encaixe":
    mod_objs = importa("novo_modulo_camera_v3.glb")
    fone_objs = importa("fone_gancho.glb")
    # boss P3 sob o modulo (recriado como no assembly)
    mat_p = bpy.data.materials.new("BossP3")
    mat_p.use_nodes = True
    mat_p.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.022, 1)
    mat_p.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.5
    bpy.ops.mesh.primitive_cylinder_add(radius=0.0045, depth=0.007, vertices=48,
                                        location=(-0.010, -0.008, -0.0215))
    boss = bpy.context.active_object
    boss.data.materials.append(mat_p)
    ee = bpy.data.objects.new("G_Fone", None)
    scene.collection.objects.link(ee)
    for o in fone_objs:
        o.parent = ee
    # modulo (+ boss) tambem anima: desce de cima ate encontrar o plug que sobe
    gm = bpy.data.objects.new("G_Mod", None)
    scene.collection.objects.link(gm)
    for o in mod_objs:
        if o.parent is None:
            o.parent = gm
    boss.parent = gm
    POS_FIM = Vector((-0.010, -0.008, -0.0465))
    POS_INI = POS_FIM + Vector((0.0, 0.0, -0.042))
    MOD_FIM = Vector((0.0, 0.0, 0.0))
    MOD_INI = Vector((0.0, 0.0, 0.05))
    luz_estudio(0.6)
    setup_render()
    # secao "uma peca so" agora e branca: fundo transparente, pagina poe o branco
    scene.render.film_transparent = True
    scene.render.image_settings.color_mode = 'RGBA'
    cam = cam_nova(75)
    # composicao deslocada p/ a direita da tela (texto respira a esquerda)
    mira(cam, (0.1166, -0.162, -0.02), (-0.0084, -0.022, -0.035))
    pasta = os.path.join(OUT, "seq_fone_encaixe")
    os.makedirs(pasta, exist_ok=True)
    quadros = [0, 45, 89] if "prova" in sys.argv else range(90)
    for f in quadros:
        t = smoothstep(f / 89.0)
        ee.location = POS_INI.lerp(POS_FIM, t)
        gm.location = MOD_INI.lerp(MOD_FIM, t)
        render_para(os.path.join(pasta, f"f{f:03d}"))
    print("OK seq_fone_encaixe:", len(list(quadros)), "frames")

elif ASSET == "montagem":
    importa("headset_montado_v3.glb")
    grupos = {o.name: o for o in scene.objects if o.type == 'EMPTY'}
    desloc = {
        "G_Modulo_Camera": Vector((0.0, -0.055, 0.0)),
        "G_Modulo_Bateria": Vector((0.0, 0.055, 0.0)),
        "G_Fone_Mic": Vector((0.0, -0.03, -0.06)),
    }
    luz_estudio(1.0)
    setup_render()
    cam = cam_nova(70)
    # mais afastada (conjunto menor, modulos inteiros) e composicao deslocada p/ a direita (card de foto a esquerda)
    # conjunto inteiro na metade direita (card de 44vw a esquerda)
    mira(cam, (0.822, -0.848, 0.434), (-0.089, -0.110, 0.0))
    pasta = os.path.join(OUT, "seq_montagem")
    os.makedirs(pasta, exist_ok=True)
    for f in range(60):
        t = smoothstep(f / 59.0)
        for nome, d in desloc.items():
            if nome in grupos:
                grupos[nome].location = d * (1.0 - t)
        render_para(os.path.join(pasta, f"f{f:03d}"))
    print("OK seq_montagem: 60 frames")

elif ASSET == "relogio_giro":
    importa("relogio.glb")
    luz_estudio(0.6)
    setup_render()
    # raios +43% => relogio ~30% menor; uma volta so, comecando/terminando na pose "legivel" (ang 300.5)
    orbita_seq("seq_relogio_giro", (0.0, 0.0, -0.01), 0.35, 0.315, math.radians(26), math.radians(22), 90, lens=70, ang0=300.5, giro=360)

elif ASSET == "final_perfil":
    importa("headset_montado_v3.glb")
    # manequim para o still final
    matp = bpy.data.materials.new("Pele")
    matp.use_nodes = True
    matp.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.35, 0.28, 0.25, 1)
    matp.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.7
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=64, ring_count=48, location=(0, 0, 0))
    cab = bpy.context.active_object
    cab.scale = (0.095, 0.0775, 0.110)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    cab.data.materials.append(matp)
    bpy.ops.object.shade_smooth()
    # luz dramatica: key dura + rim forte
    bpy.ops.object.light_add(type='AREA', location=(0.45, -0.5, 0.35))
    k = bpy.context.active_object
    k.data.energy = 16
    k.data.size = 0.25
    k.rotation_euler = (math.radians(50), math.radians(15), math.radians(40))
    bpy.ops.object.light_add(type='AREA', location=(-0.3, 0.55, 0.15))
    r = bpy.context.active_object
    r.data.energy = 20
    r.data.size = 0.18
    r.rotation_euler = (math.radians(245), math.radians(-15), 0)
    setup_render(1920, 1080, 90)
    cam = cam_nova(85)
    mira(cam, (0.10, -0.62, 0.05), (0.01, 0.0, 0.02))
    pasta = os.path.join(OUT, "stills")
    os.makedirs(pasta, exist_ok=True)
    render_para(os.path.join(pasta, "img_final_perfil"))
    print("OK final_perfil: 1 still")

else:
    print("Asset desconhecido:", ASSET)
