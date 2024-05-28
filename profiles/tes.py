from django.db.models import Count, Q
from profiles.models import User, UserRoles, Roles, UserProfiles, IsUmadjaf

# Obtenha todos os IDs de usuários na tabela User
user_ids = User.objects.values_list('id', flat=True)

# Obtenha todos os UserRoles que referenciam um ID de usuário que não existe mais
orphan_user_roles = IsUmadjaf.objects.exclude(user_id__in=user_ids)

# Imprima os IDs de usuário órfãos
for orphan_user_role in orphan_user_roles: print(orphan_user_role.user_id, 'abacate')

