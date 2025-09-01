'use client';

import React, { useState, useEffect } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { BarChart3, Plus, Download, Eye, Calendar, Users, DollarSign, TrendingUp } from 'lucide-react';

export default function RelatoriosPage() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  const stats = [
    {
      title: 'Relatórios Criados',
      value: '18',
      description: 'Relatórios personalizados',
      icon: BarChart3,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Execuções este Mês',
      value: '156',
      description: 'Relatórios executados',
      icon: TrendingUp,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Dashboards Ativos',
      value: '5',
      description: 'Painéis configurados',
      icon: BarChart3,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Widgets Criados',
      value: '24',
      description: 'Componentes de dashboard',
      icon: BarChart3,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
  ];

  const reportCategories = [
    {
      title: 'Relatórios de Membros',
      description: 'Análises sobre membros, famílias e crescimento',
      icon: Users,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      reports: [
        'Lista de Membros por Status',
        'Crescimento de Membros',
        'Aniversariantes do Mês',
        'Relatório de Visitantes',
        'Membros por Faixa Etária',
      ],
    },
    {
      title: 'Relatórios Financeiros',
      description: 'Análises financeiras e de contribuições',
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      reports: [
        'Relatório de Dízimos e Ofertas',
        'Despesas por Categoria',
        'Fluxo de Caixa',
        'Comparativo Mensal',
        'Relatório de Campanhas',
      ],
    },
    {
      title: 'Relatórios de Grupos',
      description: 'Análises sobre células, classes e ministérios',
      icon: Users,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
      reports: [
        'Frequência por Grupo',
        'Líderes e Membros',
        'Crescimento de Grupos',
        'Relatório de Reuniões',
        'Participação por Campus',
      ],
    },
    {
      title: 'Relatórios de Eventos',
      description: 'Análises sobre eventos e participação',
      icon: Calendar,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
      reports: [
        'Participação em Eventos',
        'Eventos por Período',
        'Inscrições e Presenças',
        'Relatório de Voluntários',
        'Avaliação de Eventos',
      ],
    },
  ];

  const recentReports = [
    {
      id: 1,
      name: 'Relatório Mensal de Membros',
      category: 'Membros',
      lastRun: '2025-01-15',
      status: 'Concluído',
      format: 'PDF',
    },
    {
      id: 2,
      name: 'Fluxo de Caixa - Janeiro',
      category: 'Financeiro',
      lastRun: '2025-01-14',
      status: 'Concluído',
      format: 'Excel',
    },
    {
      id: 3,
      name: 'Frequência de Grupos',
      category: 'Grupos',
      lastRun: '2025-01-13',
      status: 'Processando',
      format: 'PDF',
    },
    {
      id: 4,
      name: 'Eventos do Trimestre',
      category: 'Eventos',
      lastRun: '2025-01-12',
      status: 'Concluído',
      format: 'PDF',
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
            <h1 className="text-2xl font-bold text-gray-900">Relatórios e Dashboards</h1>
            <p className="text-gray-600">Análises e relatórios personalizados</p>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline">
              <BarChart3 className="w-4 h-4 mr-2" />
              Dashboards
            </Button>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Novo Relatório
            </Button>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <div className={`p-2 rounded-md ${stat.bgColor}`}>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
                <p className="text-xs text-gray-500 mt-1">
                  {stat.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Report Categories */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {reportCategories.map((category, index) => (
            <Card key={index} className="hover:shadow-md transition-shadow">
              <CardHeader>
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-md ${category.bgColor}`}>
                    <category.icon className={`h-6 w-6 ${category.color}`} />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{category.title}</CardTitle>
                    <CardDescription>{category.description}</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {category.reports.map((report, reportIndex) => (
                    <li key={reportIndex} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{report}</span>
                      <div className="flex space-x-1">
                        <button className="text-blue-600 hover:text-blue-800">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-green-600 hover:text-green-800">
                          <Download className="w-4 h-4" />
                        </button>
                      </div>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Recent Reports */}
        <Card>
          <CardHeader>
            <CardTitle>Relatórios Recentes</CardTitle>
            <CardDescription>
              Últimos relatórios executados no sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Nome do Relatório
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Categoria
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Última Execução
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Formato
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ações
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {recentReports.map((report) => (
                    <tr key={report.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {report.name}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                          {report.category}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(report.lastRun).toLocaleDateString('pt-BR')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          report.status === 'Concluído' ? 'bg-green-100 text-green-800' :
                          report.status === 'Processando' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {report.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {report.format}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <div className="flex items-center justify-end space-x-2">
                          <button className="text-blue-600 hover:text-blue-900">
                            <Eye className="w-4 h-4" />
                          </button>
                          <button className="text-green-600 hover:text-green-900">
                            <Download className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Quick Dashboard */}
        <Card>
          <CardHeader>
            <CardTitle>Dashboard Rápido</CardTitle>
            <CardDescription>
              Visão geral dos principais indicadores
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">1,234</div>
                <div className="text-sm text-gray-500">Total de Membros</div>
                <div className="text-xs text-green-600 mt-1">+5.2% este mês</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">R$ 45.230</div>
                <div className="text-sm text-gray-500">Receita Mensal</div>
                <div className="text-xs text-green-600 mt-1">+12.8% este mês</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">45</div>
                <div className="text-sm text-gray-500">Grupos Ativos</div>
                <div className="text-xs text-green-600 mt-1">+2 novos grupos</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
