# usuario/context_processors.py
from django.contrib.auth.models import Group
from gobierno.models import (
    MiembroGabinete,
    MiembroGabineteRegidores,
    MiembroGabineteDirectores,
    MiembroGabinetePresidentesComu,
    MiembroGabineteCoordinadoresDif,
)

def gabinete_context(request):
    """
    Contexto global:
      - is_gabinete: bool -> está en el grupo 'Gabinete'
      - gabinete_has_member: bool -> tiene asociación en algún modelo
      - gabinete_member: obj|None -> primer miembro encontrado
      - gabinete_member_model: str|None -> nombre del modelo donde se halló
    """
    ctx = {
        "is_gabinete": False,
        "gabinete_has_member": False,
        "gabinete_member": None,
        "gabinete_member_model": None,
    }

    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return ctx

    # 1) Obtener o crear el grupo "Gabinete"
    gabinete_group, _ = Group.objects.get_or_create(name="Gabinete")

    # ¿El usuario pertenece a ese grupo?
    ctx["is_gabinete"] = gabinete_group in user.groups.all()

    # 2) ¿tiene miembro asociado en alguno de los modelos?
    modelos = [
        ("MiembroGabinete", MiembroGabinete),
        ("MiembroGabineteRegidores", MiembroGabineteRegidores),
        ("MiembroGabineteDirectores", MiembroGabineteDirectores),
        ("MiembroGabinetePresidentesComu", MiembroGabinetePresidentesComu),
        ("MiembroGabineteCoordinadoresDif", MiembroGabineteCoordinadoresDif),
    ]

    for model_name, Model in modelos:
        miembro = (
            Model.objects.select_related("municipio", "dependencia")
            .filter(usuario=user)
            .first()
        )
        if miembro:
            ctx["gabinete_has_member"] = True
            ctx["gabinete_member"] = miembro
            ctx["gabinete_member_model"] = model_name
            break

    return ctx
