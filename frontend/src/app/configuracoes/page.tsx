'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useAuth } from '@/contexts/AuthContext';
import { Settings, Building2, Users, Shield, Bell, Database, Globe } from 'lucide-react';

export default function ConfiguracoesPage() {
  const { igreja, campus, user } = useAuth();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  const configSections = [
    {
      title: 'Igreja',
      description: 'Configurações gerais da igreja',
      icon: Building2,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      items: [
        'Informações básicas',
        'Logo e identidade visual',
        'Endereço e contatos',
        'Configurações de plano',
      ],
    },
    {
      title: 'Campus',
      description: 'Gerenciar campus e hierarquia',
      icon: Globe,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      items: [
        'Lista de campus',
        'Hierarquia organizacional',
        'Responsáveis por campus',
        'Configurações específicas',
      ],
    },
    {
      title: 'Usuários',
      description: 'Gestão de usuários e permissões',
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      items: [
        'Lista de usuários',
        'Papéis e permissões',
        'Níveis de acesso',
        'Auditoria de ações',
      ],
    },
    {
      title: 'Segurança',
      description: 'Configurações de segurança',
      icon: Shield,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
      items: [
        'Políticas de senha',
        'Autenticação em dois fatores',
        'Logs de segurança',
        'Backup e recuperação',
      ],
    },
    {
      title: 'Notificações',
      description: 'Configurar alertas e notificações',
      icon: Bell,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
      items: [
        'Notificações por email',
        'Alertas do sistema',
        'Lembretes automáticos',
        'Configurações de frequência',
      ],
    },
    {
      title: 'Sistema',
      description: 'Configurações técnicas do sistema',
      icon: Database,
      color: 'text-gray-600',
      bgColor: 'bg-gray-100',
      items: [
        'Backup automático',
        'Integração com APIs',
        'Configurações de email',
        'Logs do sistema',
      ],
    },
  ];

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Configurações</h1>
            <p className="text-gray-600">Gerencie as configurações do sistema</p>
          </div>
          <Button variant="outline">
            <Settings className="w-4 h-4 mr-2" />
            Configurações Avançadas
          </Button>
        </div>

        {/* Current Context */}
        <Card>
          <CardHeader>
            <CardTitle>Contexto Atual</CardTitle>
            <CardDescription>
              Informações sobre sua igreja e campus atual
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Igreja
                </label>
                <div className="text-lg font-semibold text-gray-900">
                  {igreja?.nome || 'Não definida'}
                </div>
                <div className="text-sm text-gray-500">
                  Plano: {igreja?.plano || 'N/A'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Campus
                </label>
                <div className="text-lg font-semibold text-gray-900">
                  {campus?.nome || 'Não definido'}
                </div>
                <div className="text-sm text-gray-500">
                  Nível: {campus?.nivel || 'N/A'}
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Usuário
                </label>
                <div className="text-lg font-semibold text-gray-900">
                  {user?.first_name} {user?.last_name}
                </div>
                <div className="text-sm text-gray-500">
                  Nível de acesso: {user?.nivel_acesso || 'N/A'}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Configuration Sections */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {configSections.map((section, index) => (
            <Card key={index} className="hover:shadow-md transition-shadow cursor-pointer">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-md ${section.bgColor}`}>
                    <section.icon className={`h-6 w-6 ${section.color}`} />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{section.title}</CardTitle>
                    <CardDescription>{section.description}</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {section.items.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{item}</span>
                      <button className="text-blue-600 hover:text-blue-800 text-sm">
                        Configurar
                      </button>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Configurações Rápidas</CardTitle>
            <CardDescription>
              Ajustes mais comuns do sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome da Igreja
                  </label>
                  <Input
                    value={igreja?.nome || ''}
                    placeholder="Nome da igreja"
                    disabled
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Principal
                  </label>
                  <Input
                    value={igreja?.email || ''}
                    placeholder="email@igreja.com"
                    disabled
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Telefone
                  </label>
                  <Input
                    value={igreja?.telefone || ''}
                    placeholder="(11) 99999-9999"
                    disabled
                  />
                </div>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Site da Igreja
                  </label>
                  <Input
                    value={igreja?.site || ''}
                    placeholder="https://www.igreja.com"
                    disabled
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    CNPJ
                  </label>
                  <Input
                    value={igreja?.cnpj || ''}
                    placeholder="00.000.000/0001-00"
                    disabled
                  />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    Igreja Ativa
                  </span>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    igreja?.ativa ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {igreja?.ativa ? 'Ativa' : 'Inativa'}
                  </span>
                </div>
              </div>
            </div>
            <div className="mt-6 flex justify-end">
              <Button disabled>
                Salvar Alterações
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* System Information */}
        <Card>
          <CardHeader>
            <CardTitle>Informações do Sistema</CardTitle>
            <CardDescription>
              Detalhes técnicos e limites do plano
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <div className="text-sm font-medium text-gray-700">Limite de Membros</div>
                <div className="text-2xl font-bold text-blue-600">
                  {igreja?.limite_membros || 0}
                </div>
                <div className="text-xs text-gray-500">membros permitidos</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">Limite de Mensagens</div>
                <div className="text-2xl font-bold text-green-600">
                  {igreja?.limite_mensagens || 0}
                </div>
                <div className="text-xs text-gray-500">mensagens por mês</div>
              </div>
              <div>
                <div className="text-sm font-medium text-gray-700">Armazenamento</div>
                <div className="text-2xl font-bold text-purple-600">
                  {igreja?.limite_storage ? `${(igreja.limite_storage / 1024 / 1024 / 1024).toFixed(1)}GB` : '0GB'}
                </div>
                <div className="text-xs text-gray-500">espaço disponível</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
